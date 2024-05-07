import json
import os
import sys
import time

from loguru import logger
import psycopg

file = sys.argv[1]

with open(f"{os.path.abspath(os.curdir)}/bot/scripts/sql/{file}") as sql_file:
    text = sql_file.read()
    commands = text.split('\n')
    commands_count = len(commands)
    
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
                if index == 0:
                    logger.info(f'{db_host}:{db_port} - Insertion started')
                elif index%900 == 0:
                    percent = index/commands_count*100
                    logger.info(f'{db_host}:{db_port} - Insertion is {int(percent)}% complete')
                time.sleep(0.5)
        logger.info(f'{db_host}:{db_port} - Inserts {file} complete')
            
except psycopg.OperationalError as error:
    logger.error(f"{db_host}:{db_port} - {error}")