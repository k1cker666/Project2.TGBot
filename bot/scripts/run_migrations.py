import os
import psycopg
from loguru import logger
import json

directory = f"{os.path.abspath(os.curdir)}/bot/migrations/"
migrations = os.listdir(directory)
migrations.sort()

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