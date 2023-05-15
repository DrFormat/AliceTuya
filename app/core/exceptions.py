from typing import Optional

from fastapi import HTTPException


class ConflictDBException(Exception):
    def __init__(self) -> None:
        super(ConflictDBException, self).__init__()


class NotFoundException(Exception):
    def __init__(self, title: Optional[str] = ''):
        msg = 'Not Found'
        super(NotFoundException, self).__init__(f'{title} {msg}' if title else msg)


class ConflictException(HTTPException):
    def __init__(self) -> None:
        super(ConflictException, self).__init__(status_code=409, detail='Conflict Error')


class DeleteException(HTTPException):
    def __init__(self) -> None:
        super(DeleteException, self).__init__(status_code=400, detail='Link exist. Can\'t remove')


class InvalidUsageException(HTTPException):
    def __init__(self) -> None:
        super(InvalidUsageException, self).__init__(status_code=422)


class MoreOneException(HTTPException):
    def __init__(self) -> None:
        super(MoreOneException, self).__init__(status_code=500, detail='Result more than one')


class ExternalIDException(HTTPException):
    def __init__(self) -> None:
        super(ExternalIDException, self).__init__(status_code=500, detail='ExternalID not found')


class NoImplementationException(HTTPException):
    def __init__(self) -> None:
        super(NoImplementationException, self).__init__(status_code=501, detail='Not Implemented')


class WebServerIsDownException(HTTPException):
    def __init__(self, e) -> None:
        super(WebServerIsDownException, self).__init__(status_code=521, detail=e)
