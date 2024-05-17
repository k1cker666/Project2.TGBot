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


# @app.get("/check_pg/")
# def check_pg_connection():
#     try:
#         connection = deps.postgres.connection_pool.getconn()
#     except psycopg.OperationalError:
#         return {"pg_connection": False}
#     else:
#         params = connection.info.get_parameters()
#         deps.postgres.connection_pool.putconn(connection)
#         return {"pg_connection": True, "connection_info": params}


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
