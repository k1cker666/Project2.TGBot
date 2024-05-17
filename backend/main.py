import uuid

import psycopg
from fastapi import FastAPI
from redis.exceptions import ConnectionError
from src.dependencies import DependenciesBuilder
from src.log import logger_config, logger_main


logger_config
logger_main

deps = DependenciesBuilder.build()
redis = deps.redis.connection


app = FastAPI()


@app.get("/check_pg/")
def check_pg_connection():
    try:
        connection = deps.postgres.connection_pool.getconn()
    except psycopg.OperationalError:
        return {"pg_connection": False}
    else:
        params = connection.info.get_parameters()
        deps.postgres.connection_pool.putconn(connection)
        return {"pg_connection": True, "connection_info": params}


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
    redis.set(name=str(uuid_token), value=tg_login)
    return {"tg_login": tg_login, "uuid_token": uuid_token}
