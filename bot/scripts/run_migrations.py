import os
import psycopg
from loguru import logger

directory = f"{os.path.abspath(os.curdir)}/bot/migrations/"
migrations = os.listdir(directory)
migrations.sort()

try:
    db_name = 'tgbot'
    db_user = 'postgres'
    db_password = 'roma1234'
    db_host = 'localhost' #'postgres'/'localhost'
    db_port =  "5432"
    with psycopg.connect(
        user = db_user,
        password = db_password,
        host = db_host, 
        port = db_port,
        autocommit = True) as conn:
        logger.info(f'{db_host}:{db_port} - Connection to PostgreSQL as user {db_user} successful')
        with conn.cursor() as cur:
            cur.execute("select 1 from pg_database where datname = 'tgbot';")
            result = cur.fetchone()
            if result == None:
                cur.execute('create database tgbot;')
                logger.info(f'{db_host}:{db_port} - Database {db_name} created')
            else:
                logger.info(f'{db_host}:{db_port} - Database {db_name} already exists')
            
    with psycopg.connect(
        dbname = db_name,
        user = db_user,
        password = db_password,
        host = db_host, 
        port = db_port,
        autocommit = True) as conn:
        logger.info(f'{db_host}:{db_port} - Connection to {db_name} database as user {db_user} successful')
        
        with conn.cursor() as cur:
            for file in migrations:
                path =f'{directory}{file}'

                with open(path, 'r') as command:
                    cur.execute(command.read())
                    logger.info(f'{db_host}:{db_port} - Migration {file} complete')

except Exception as error:    
    logger.error(f"{error}")