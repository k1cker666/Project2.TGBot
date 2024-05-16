import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI
import psycopg


load_dotenv()

db_name = os.getenv("PSQL_DBNAME")
db_user = os.getenv("PSQL_USER")
db_password = os.getenv("PSQL_PASSWORD")
db_host = os.getenv("PSQL_HOST")
db_port = os.getenv("PSQL_PORT")
ff = os.getenv("PSQL_POOL_MAX_SIZE")

app = FastAPI()


@app.get("/")
def check_pg_connection():
    try:
        connection = psycopg.connect(
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
    except psycopg.OperationalError as e:
        return {"connection" : False}
    else:
        params = connection.info.get_parameters()
        connection.close()
        return {"connection" : True, "connection_info" : params}


@app.get("/get_token/")
def get_token(tg_login: str):
    uuid_token = uuid.uuid5(uuid.NAMESPACE_DNS, tg_login)
    return {"tg_login": tg_login, "uuid_token": uuid_token}
