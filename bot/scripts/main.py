import os
import subprocess

import psycopg
from dotenv import load_dotenv
from loguru import logger


load_dotenv()


db_name = os.getenv("PSQL_DBNAME")
db_user = os.getenv("PSQL_USER")
db_password = os.getenv("PSQL_PASSWORD")
db_host = os.getenv("PSQL_HOST")
db_port = os.getenv("PSQL_PORT")


def check_db():
    try:
        connect = psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except psycopg.OperationalError:
        logger.info(
            f"{db_host}:{db_port} - Database {db_name} is not available"
        )
        return False
    else:
        connect.close()
        return True


def run_migrations():
    try:
        result = subprocess.run(
            ["python3", "bot/scripts/run_migrations.py"], check=True
        )
        logger.info(
            f"Migrations complete with return code {result.returncode}"
        )
    except subprocess.CalledProcessError as e:
        logger.info(f"Error output: {e.output}")


def run_sql():
    try:
        result = subprocess.run(
            [
                "python3",
                "bot/scripts/run_sql.py",
                "--file=insert_word_dataset.sql",
            ],
            check=True,
        )
        logger.info(
            f"Migrations complete with return code {result.returncode}"
        )
    except subprocess.CalledProcessError as e:
        logger.info(f"Error output: {e.output}")


if __name__ == "__main__":
    if check_db:
        run_migrations()
        run_sql()
