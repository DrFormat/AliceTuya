import datetime
import random
import string
import time
from typing import Union, Optional

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import APIRouter, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response, JSONResponse
from fastapi.security import HTTPBearer
from starlette.requests import Request

from app.core.exceptions import NotFoundException
from app.database.schemas import OAuth2AuthorizationCode, OAuth2AuthorizationCodeCreateUpdate, User
from app.database.schemas.oauth2 import OAuth2TokenCreateUpdate, OAuth2Token
from app.datasources.oauth2_datasource import OAuth2Datasource, get_oauth2_ds
from app.repositories.user_repository_impl import UserRepositoryImpl, get_user_repo

router = APIRouter(redirect_slashes=True, prefix='/o', tags=['OAuth2'])

db_table_params = {}

db_table_tokens = {}
db_table_refresh_tokens = {}
rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

pem_private_key = encrypted_pem_private_key = rsa_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

pem_public_key = rsa_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print('generated public key')
print(pem_public_key.decode('ascii'))

auth_scheme = HTTPBearer(auto_error=False)


async def authorized(token: str = Depends(auth_scheme),
                     oauth2_ds: OAuth2Datasource = Depends(get_oauth2_ds)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token:
        obj = await oauth2_ds.get_token(getattr(token, 'credentials'), 'access_token')
        if obj:
            return OAuth2Token.from_orm(obj)
    raise credentials_exception


def as_jwt(data=None):
    if data is None:
        data = {}
    result = jwt.encode(data, pem_private_key, algorithm="RS256")
    return result


def random_string(size=32) -> str:
    return ''.join((random.choice(string.ascii_letters + string.digits) for _ in range(size)))


def create_token(client_state='', expires_in=3600, refresh_token_expires_in=24 * 3600) -> dict:
    code = "C-" + random_string()
    accesstoken = "ACCT-" + random_string()
    refreshtoken = "REFT-" + random_string()
    id_token = "IDT-" + random_string()
    date_of_creation = datetime.datetime.now(tz=datetime.timezone.utc)
    result = {
        'id_token': id_token,

        'access_token': accesstoken,
        'date_of_creation': date_of_creation,
        'expires_in': expires_in,

        'refresh_token': refreshtoken,
        'refresh_token_expires_in': date_of_creation + datetime.timedelta(refresh_token_expires_in),

        'code': code,
        'state': client_state,
        'token_type': "Bearer",

        'exp': date_of_creation + datetime.timedelta(seconds=expires_in)
    }
    return result


def extract_keys(data=None, keys=None) -> dict | str:
    if keys is None:
        keys = []
    if data is None:
        data = {}
    result = {}
    for key in keys:
        value = data.get(key, None)
        if value is not None:
            result[key] = value
    return result


def login_page(request: Request, verify_key=None, suggested_users=None) -> str:
    if suggested_users is None:
        suggested_users = []
    if verify_key is None:
        verify_key = random_string()

    if len(suggested_users) == 0:
        user_help = ''
    else:
        user_help = 'Try to use one of emails: ' + ', '.join(suggested_users)

    return request.app.tmpl.TemplateResponse('login.html', {'request': request, 'verify_key': verify_key})


@router.get('/login')
async def get_login_page(request: Request,
                         response_type: Union[str, None] = 'code',
                         client_id: Union[str, None] = 'SomeClientID',
                         state: Union[str, None] = 'SomeState',
                         redirect_uri: Union[str, None] = 'redirectURL',
                         oauth2_ds: OAuth2Datasource = Depends(get_oauth2_ds)):
    # if there is a sign that user is already logged in, then appropriate redirect should be returned (see method postNameAndPassword)

    application = await oauth2_ds.get_app_by_client_id(client_id)
    if not application:
        return request.app.tmpl.TemplateResponse('error.html', {'request': request, 'msg': 'client_id'})

    if application.authorization_grant_type != 'authorization_code' and response_type != 'code':
        return request.app.tmpl.TemplateResponse('error.html', {'request': request, 'msg': 'response_type'})
    if redirect_uri != application.redirect_uris:
        return request.app.tmpl.TemplateResponse('error.html', {'request': request, 'msg': 'redirect_uri'})

    stored_params = {
        "response_type": response_type,
        "client_id": client_id,
        "state": state,
        "redirect_uri": redirect_uri
    }

    # here client_id should be checked
    # here redirect_uri should be checked (client should use always same redirect uri)

    # save info into db table
    verify_key = random_string()
    db_table_params[verify_key] = stored_params

    # return login page

    return login_page(request, verify_key)


@router.post('/login')
async def post_name_and_password(request: Request,
                                 username: str = Form(None), password: str = Form(None),
                                 verify_key: str = Form(None),
                                 repo: UserRepositoryImpl = Depends(get_user_repo),
                                 oauth2_ds: OAuth2Datasource = Depends(get_oauth2_ds)):
    # username and password must be checked here, if they match eachother

    # retrieve previously stored data from db table
    stored_params = db_table_params.get(verify_key, None)
    if (stored_params is None) or (verify_key is None):
        # login has not been initiated appropriatelly
        HTMLResponse(content=f"Bad OAuth Flow, {verify_key} has not been found", status_code=404)

    try:
        user = await repo.get_by_username(username)
    except NotFoundException:
        return login_page(request, verify_key)

    if user.password != password:
        return login_page(request, verify_key)

    # remove stored data from table
    del db_table_params[verify_key]  # remove key from table

    # store code and related info into db table
    oauth2_codes = OAuth2AuthorizationCodeCreateUpdate(
        code=random_string(),
        client_id=stored_params['client_id'],
        redirect_uri=stored_params['redirect_uri'],
        user_id=user.id
    )
    # code = random_string()
    a = await oauth2_ds.create_authorization_code(oauth2_codes)
    # a = await oauth2_ds.get_authorization_code(oauth2_codes.code)
    stored_params['user'] = username
    # db_table_codes[oauth2_codes.code] = stored_params
    if '?' in oauth2_codes.redirect_uri:
        url = f"{oauth2_codes.redirect_uri}&code={oauth2_codes.code}&state={stored_params['state']}"
    else:
        url = f"{oauth2_codes.redirect_uri}" \
              f"?code={oauth2_codes.code}" \
              f"&state={stored_params['state']}" \
              f"&client_id={oauth2_codes.client_id}"
    return RedirectResponse(url, status_code=status.HTTP_302_FOUND)


@router.post('/token')
async def exchange_code_for_token(
        response: Response,
        grant_type: str = Form(None), code: str = Form(None), client_id: str = Form(None),
        client_secret: Optional[str] = Form(None),
        code_verifier: Optional[str] = Form(None),
        refresh_token: Optional[str] = Form(None),
        oauth2_ds: OAuth2Datasource = Depends(get_oauth2_ds)):
    # add header Cache-Control: no-store
    response.headers["Cache-Control"] = "no-store"

    # if web app flow is used, client_secret should be checked
    # if PKCE flow is used, code_verifier must be returned

    if grant_type == 'authorization_code':
        # retrieve previously stored data from db table
        # stored_params = db_table_codes.get(code, None)
        obj = await oauth2_ds.get_authorization_code(code)
        oauth2_code: OAuth2AuthorizationCode = OAuth2AuthorizationCode.from_orm(obj)
        if oauth2_code is None:
            # login has not been initiated appropriatelly
            print(f'[authorization_code] Bad OAuth Flow, code {code} has not been found')
            return JSONResponse(content={
                'error': 'invalid_request',
                'error_description': f'Bad OAuth Flow, code {code} has not been found'
            }, status_code=404)

        # del db_table_codes[code]  # delete code, so it is not possible to use it more?

        token = create_token()
        obj = OAuth2TokenCreateUpdate(
            client_id=oauth2_code.client_id,
            token_type=token['token_type'],
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            issued_at=token['date_of_creation'].timestamp(),
            exp=token['expires_in'],
            user_id=oauth2_code.user_id
        )
        await oauth2_ds.create_token(obj)

        token_row = {**token, **oauth2_code.dict()}
        # db_table_tokens[token_row['access_token']] = token_row
        # db_table_refresh_tokens[token_row['refresh_token']] = token_row

        response_json = extract_keys(token_row, ['token_type', 'access_token', 'expires_in', 'refresh_token'])
        pass

    if grant_type == 'refresh_token':
        obj = await oauth2_ds.get_token(refresh_token, 'refresh_token')
        # stored_params = db_table_refresh_tokens.get(refresh_token, None)
        if obj is None:
            # refresh token does not exist
            print(f'[refresh_token] Bad OAuth Flow, refresh_token {refresh_token} has not been found')
            return JSONResponse(content={
                'error': 'invalid_request',
                'error_description': f'Bad OAuth Flow, refresh_token {refresh_token} has not been found'
            }, status_code=404)

        # remove token from tables
        # del db_table_tokens[token_row['access_token']]
        # del db_table_refresh_tokens[token_row['refresh_token']]

        oauth2_token: OAuth2Token = OAuth2Token.from_orm(obj)
        if oauth2_token.is_revoked():
            # refresh token has expired
            print(f'[refresh_token_expires_in] Bad OAuth Flow, refresh_token {refresh_token} has not been found')
            return JSONResponse(content={
                'error': 'invalid_refresh_token',
                'error_description': f'Bad OAuth Flow, refresh_token {refresh_token} has been revoked'
            }, status_code=403)

        oauth2_token.access_token_revoked_at = int(time.time())
        oauth2_token.refresh_token_revoked_at = int(time.time())
        await oauth2_ds.update_token(oauth2_token.id, oauth2_token)

        token = create_token()
        obj = OAuth2TokenCreateUpdate(
            client_id=oauth2_token.client_id,
            token_type=token['token_type'],
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            issued_at=token['date_of_creation'].timestamp(),
            exp=token['expires_in'],
            user_id=oauth2_token.user_id
        )
        await oauth2_ds.create_token(obj)

        token_row = {**token}
        db_table_tokens[token_row['access_token']] = token_row
        db_table_refresh_tokens[token_row['refresh_token']] = token_row

        response_json = extract_keys(token_row, ['token_type', 'access_token', 'expires_in', 'refresh_token'])
        pass

    if code_verifier is not None:
        # PKCE flow
        response_json[code_verifier] = code_verifier

    print(f'[response_json] {response_json}')
    return response_json


@router.get('/userinfo', response_model=User, dependencies=[Depends(authorized)])
async def get_user_info(token=Depends(authorized), user_repo: UserRepositoryImpl = Depends(get_user_repo)):
    if token is None:
        # login has not been initiated appropriatelly
        return JSONResponse(content={
            'error': 'invalid_request',
            'error_description': f'Bad OAuth Flow, token {token} has not been found'
        }, status_code=404)
    user = await user_repo.get(token.user_id)
    return user
    # return as_jwt(response_json)


@router.get('/logout', dependencies=[Depends(authorized)])
async def logout(token=Depends(authorized), oauth2_ds: OAuth2Datasource = Depends(get_oauth2_ds)):
    token.access_token_revoked_at = int(time.time())
    token.refresh_token_revoked_at = int(time.time())
    await oauth2_ds.update_token(token.id, token)
    # where to go?
    return RedirectResponse('/auth/login')


@router.get('/publickey')
async def get_public_key_pem():
    return pem_public_key.decode('ascii')
