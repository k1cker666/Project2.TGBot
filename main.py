import os

import click
import psycopg
import redis
from dotenv import load_dotenv
from loguru import logger


load_dotenv()


psql_db_name = os.getenv("PSQL_DBNAME")
psql_db_user = os.getenv("PSQL_USER")
psql_db_password = os.getenv("PSQL_PASSWORD")
psql_db_host = os.getenv("PSQL_HOST")
psql_db_port = os.getenv("PSQL_PORT")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")


def check_pg():
    try:
        connect = psycopg.connect(
            dbname=psql_db_name,
            user=psql_db_user,
            password=psql_db_password,
            host=psql_db_host,
            port=psql_db_port,
        )
    except psycopg.OperationalError:
        logger.info(
            f"{psql_db_host}:{psql_db_port} - Database {psql_db_name} is not available"
        )
        return False
    else:
        connect.close()
        return True


def check_redis():
    connect = redis.Redis(
        host=redis_host,
        port=redis_port,
    )
    try:
        connect.ping()
    except ConnectionError:
        logger.info(
            f"{redis_host}:{redis_port} - Redis database is not available"
        )
        return False
    else:
        connect.close()
        return True


@click.command()
@click.option("--service", help="Name of service(tgbot/backend)")
def start_service(service_name: str):
    if check_pg() and check_redis():
        if service_name == "tgbot":
            os.system("python3 project/bot/main.py")
        if service_name == "backend":
            os.system("fastapi dev project/backend/main.py")
