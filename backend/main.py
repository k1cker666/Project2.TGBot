import uuid

import psycopg
from fastapi import FastAPI
from src.dependencies import DependenciesBuilder
from src.log import logger_config, logger_main


logger_config
logger_main

deps = DependenciesBuilder.build()


app = FastAPI()


@app.get("/")
def check_pg_connection():
    try:
        connection = deps.postgres.connection_pool.getconn()
    except psycopg.OperationalError:
        return {"connection": False}
    else:
        params = connection.info.get_parameters()
        deps.postgres.connection_pool.putconn(connection)
        return {"connection": True, "connection_info": params}


@app.get("/get_token/")
def get_token(tg_login: str):
    uuid_token = uuid.uuid5(uuid.NAMESPACE_DNS, tg_login)
    return {"tg_login": tg_login, "uuid_token": uuid_token}
