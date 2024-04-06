import os
import psycopg
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger('migrations')

directory = f"{os.path.abspath(os.curdir)}/bot/migrations/"
migrations = os.listdir(directory)
migrations.sort()

try:
    with psycopg.connect(
        user = 'postgres',
        password = 'roma1234',
        host = 'localhost', #'postgres'/'localhost'
        port = '5432',
        autocommit = True) as conn:
        logger.info('Connection to PostgreSQL successful')
        with conn.cursor() as cur:
            cur.execute("select 1 from pg_database where datname = 'tgbot';")
            result = cur.fetchone()
            if result == None:
                cur.execute('create database tgbot;')
                logger.info('Database tgbot created')
            else:
                logger.info('Database tgbot already exists')
            
    with psycopg.connect(
        dbname = 'tgbot',
        user = 'postgres',
        password = 'roma1234',
        host = 'localhost', #'postgres'/'localhost'
        port = '5432',
        autocommit = True) as conn:
        logger.info('Connection to tgbot database successful')
        
        with conn.cursor() as cur:
            for file in migrations:
                path =f'{directory}{file}'

                with open(path, 'r') as command:
                    cur.execute(command.read())
                    logger.info(f'Migration {file} complete')

except Exception as error:    
    logger.error(f"{error}")