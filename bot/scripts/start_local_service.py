import json
import os
import time

from loguru import logger
import psycopg

def start_local_service():
    with open(f"{os.path.abspath(os.curdir)}/bot/scripts/sql/local_service.sql") as sql_file:
        text = sql_file.read()
        commands = text.split('\n')

    json_dir = f"{os.path.abspath(os.curdir)}/bot/config/config.json"
    with open(json_dir, 'r') as file:
        config = json.load(file)['psql']

    try:
        db_name = config['dbname']
        db_user = config['user']
        db_password = config['password']
        db_host = config['host']
        db_port =  config['port']
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
                    time.sleep(0.3)
            logger.info(f'{db_host}:{db_port} - Local service is ready')

    except psycopg.OperationalError as error:
        logger.error(f"{db_host}:{db_port} - {error}")
    except psycopg.errors.ForeignKeyViolation as error:
        logger.error(f"{db_host}:{db_port} - {error}")
        
if __name__ == '__main__':
    start_local_service()