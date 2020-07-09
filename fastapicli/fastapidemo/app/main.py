import sys
import asyncio
import signal
import peewee

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from cms.core.error_handler import ErrorHandler
from cms.app import api_router
from cms.core import config
from cms.core.db import get_session
from cms.core.logger import Logger
from cms.logic.register import register


logger = Logger().getLogger()

app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")

# CORS
origins = ["http://localhost:8081"]



async def shutdown(signal: signal):
    """
    彻底关闭服务, 释放端口资源
    """
    logger.info("Received exit signal %s...", signal.name)
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logger.info("Canceling outstanding tasks")
    await asyncio.gather(*tasks)



# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.include_router(api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    pgdb = get_session()
    request.state.pgdb = pgdb
    try:
        if pgdb.database.is_closed():
            logger.info('DB connecting..')
            pgdb.database.connect()

        response = await call_next(request)
        pgdb.database.close()
        return response
    except peewee.OperationalError:
        logger.info('DB reconnecting..')
        pgdb.database.connect()
        response = await call_next(request)
        return response
    except peewee.InterfaceError:
        logger.info("DB Interface Error")
        pass
    except Exception as e:
        ttype, tvalue, ttraceback = sys.exc_info()
        return ErrorHandler.handler(e, ttype, tvalue, ttraceback)



@app.on_event("startup")
async def startup():
    logger.info('startup')
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s)))

    register()
    logger.info('startup end')



# if __name__ == '__main__' and config.DEBUG:
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=80, debug=True)
