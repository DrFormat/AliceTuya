import os
import sys
from functools import lru_cache
from typing import Tuple, Optional

from pydantic import BaseSettings

app_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(app_dir, os.pardir))


class AppConfig(BaseSettings):
    APP_NAME: Optional[str] = 'dialog'
    APP_URL_PREFIX: str = '/api'

    ACCESS_ID: str
    ACCESS_SECRET: str
    ENDPOINT_URL: str
    ENDPOINT_URL_SCHEME: str = 'https://'
    MQ_ENDPOINT: str
    UID: str
    USERNAME: str
    PASSWORD: str
    SKILL_ID: str
    SKILL_TOKEN: str

    OAUTH2_ACCESS_TOKEN_GENERATOR: bool = True
    OAUTH2_REFRESH_TOKEN_GENERATOR: bool = False
    OAUTH2_TOKEN_EXPIRES_IN: int = 3600
    OAUTH2_SCOPES_SUPPORTED: list = []
    OAUTH2_ERROR_URIS: list = []

    DB_DSN: str = 'sqlite+aiosqlite:///./sql_app.db'
    REDIS_DSN: str = ''
    REDIS_PREFIX: str = 'fastapi-cache'
    # AMQP_CONNECTION: str
    # AMQP_EXCHANGE: str
    # AMQP_QUEUE: str
    AMQP_PREFETCH_COUNT: Optional[int] = 1

    APP_DIR: str = app_dir
    PROJECT_ROOT: str = project_root

    TESTING: bool = True if 'pytest' in sys.modules else False
    DEBUG: bool = False
    ENVIRONMENT: str = 'production'

    API_TITLE: str = 'Alice API'
    API_VERSION: Optional[str] = '1.0.0'
    API_DESCRIPTION: Optional[str] = 'Навыки Алисы'
    API_SECURITY: Tuple[dict] = ({'HeaderAccessToken': []},)
    API_SECURITY_DEFINITIONS = {
        'HeaderAccessToken': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'authorization'
        }
    }

    class Config:
        env_file = '.env', '../.env'


@lru_cache
def get_settings() -> AppConfig:
    settings = AppConfig()
    return settings


config = get_settings()

# DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=1)
# DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=16)
# DB_ECHO = config("DB_ECHO", cast=bool, default=False)
# DB_SSL = config("DB_SSL", default=None)
# DB_USE_CONNECTION_FOR_REQUEST = config(
#     "DB_USE_CONNECTION_FOR_REQUEST", cast=bool, default=True
# )
# DB_RETRY_LIMIT = config("DB_RETRY_LIMIT", cast=int, default=32)
# DB_RETRY_INTERVAL = config("DB_RETRY_INTERVAL", cast=int, default=1)
