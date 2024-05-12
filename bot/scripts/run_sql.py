import os
import time

import click
import psycopg
from dotenv import load_dotenv
from loguru import logger


load_dotenv()


@click.command()
@click.option("--file", help="Name of file in folder /bot/scripts/sql/")
def run_sql(file):
    with open(
        f"{os.path.abspath(os.curdir)}/bot/scripts/sql/{file}"
    ) as sql_file:
        text = sql_file.read()
        commands = text.split("\n")
        commands_count = len(commands)

    try:
        db_name = os.getenv("PSQL_DBNAME")
        db_user = os.getenv("PSQL_USER")
        db_password = os.getenv("PSQL_PASSWORD")
        db_host = os.getenv("PSQL_HOST")
        db_port = os.getenv("PSQL_PORT")
        with psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            autocommit=True,
        ) as conn:
            logger.info(
                f"{db_host}:{db_port} - Connection to {db_name} database as user {db_user} successful"
            )
            with conn.cursor() as cur:
                for index, command in enumerate(commands):
                    cur.execute(command)
                    if index == 0:
                        logger.info(f"{db_host}:{db_port} - Insertion started")
                    elif index % 900 == 0:
                        percent = index / commands_count * 100
                        logger.info(
                            f"{db_host}:{db_port} - Insertion is {int(percent)}% complete"
                        )
                    time.sleep(0.5)
            logger.info(f"{db_host}:{db_port} - Inserts {file} complete")

    except psycopg.OperationalError as error:
        logger.error(f"{db_host}:{db_port} - {error}")


if __name__ == "__main__":
    run_sql()
