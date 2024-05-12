import os
import time

from loguru import logger
import psycopg
from dotenv import load_dotenv

load_dotenv()

def start_local_service():
    with open(f"{os.path.abspath(os.curdir)}/bot/scripts/sql/local_service.sql") as sql_file:
        text = sql_file.read()
        commands = text.split('\n')
        commands_count = len(commands)
    progress_points=[int(commands_count/4), int(commands_count/4*2), int(commands_count/4*3), commands_count-1]
    try:
        db_name = os.getenv('PSQL_DBNAME')
        db_user = os.getenv('PSQL_USER')
        db_password = os.getenv('PSQL_PASSWORD')
        db_host = os.getenv('PSQL_HOST')
        db_port = os.getenv('PSQL_PORT')
        with psycopg.connect(
            dbname = db_name,
            user = db_user,
            password = db_password,
            host = db_host, 
            port = db_port,
            autocommit = True) as conn:
            logger.info(f'{db_host}:{db_port} - Connection to {db_name} database as user {db_user} successful')
            with conn.cursor() as cur:
                for index, command in enumerate(commands):
                    cur.execute(command)
                    if index in progress_points:
                        percent = index/commands_count*100
                        logger.info(f'{db_host}:{db_port} - Service is {int(percent)}% complete')
                    time.sleep(0.3)
            logger.info(f'{db_host}:{db_port} - Local service is ready')

    except psycopg.OperationalError as error:
        logger.error(f"{db_host}:{db_port} - {error}")
    except psycopg.errors.ForeignKeyViolation as error:
        logger.error(f"{db_host}:{db_port} - {error}")
        
if __name__ == '__main__':
    start_local_service()