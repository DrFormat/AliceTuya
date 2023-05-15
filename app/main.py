import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tuya_iot import TUYA_LOGGER

from app.core.config import config
from app.core.static_files import SPAStaticFiles
from app.tuya_adapter import TuyaAdapder
from app.views.auth import router as auth_router
from app.views.v1.index import router as v1_router

# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TUYA_LOGGER.setLevel(logging.DEBUG)

app = FastAPI(title=config.API_TITLE, description=config.API_DESCRIPTION, version=config.API_VERSION)


def get_app() -> FastAPI:
    app.include_router(auth_router)
    app.include_router(v1_router)
    app.mount('/static', SPAStaticFiles(directory='app/static', html=True), name='app')

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origins=["*"],
    )
    return app


@app.on_event('startup')
async def startup_event() -> None:
    logger.info('Initializing API ...')

    # loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    app.config = config
    # redis = aioredis.from_url(config.REDIS_DSN, encoding="utf8", decode_responses=True)
    # FastAPICache.init(RedisBackend(redis), prefix=config.REDIS_PREFIX)

    logger.info('Create Tuya Cloud Client')
    # Init
    tuya = TuyaAdapder(endpoint=f'{config.ENDPOINT_URL_SCHEME}{config.ENDPOINT_URL}',
                       access_id=config.ACCESS_ID, access_secret=config.ACCESS_SECRET,
                       username=config.USERNAME, password=config.PASSWORD)
    app.tcc = tuya


@app.on_event('shutdown')
async def shutdown_event():
    logger.info('Shutting down API')

    if not config.TESTING:
        logger.info('Close Tuya Cloud Client')
        if hasattr(app, 'tcc'):
            del app.tcc.openmq
