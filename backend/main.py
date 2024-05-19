import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.exceptions import ConnectionError
from src.dependencies import Dependencies, DependenciesBuilder
from src.log import logger_config, logger_main


deps: Dependencies


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_config
    logger_main
    global deps
    deps = DependenciesBuilder.build()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/check_pg/")
def check_pg_connection():
    if deps.postgres.check_connect():
        return {"pg_connection": True}
    return {"pg_connection": False}


@app.get("/check_redis/")
def check_redis_connection():
    try:
        deps.redis.connection.ping()
        return {"redis_connection": True}
    except ConnectionError:
        return {"redis_connection": False}


@app.get("/get_token/")
def get_token(tg_login: str):
    uuid_token = uuid.uuid5(uuid.NAMESPACE_DNS, tg_login)
    deps.redis.set_token(tg_login=tg_login, uuid_token=str(uuid_token))
    return {"tg_login": tg_login, "uuid_token": str(uuid_token)}


@app.get("/authorization/")
def auth(uuid_token: str):
    return {"authorization": True, "uuid_token": uuid_token}
