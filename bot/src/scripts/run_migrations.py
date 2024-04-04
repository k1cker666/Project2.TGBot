import os
import psycopg
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger('migrations')

directory = f"{os.path.abspath(os.curdir)}/bot/src/migrations/"
migrations = os.listdir(directory)
migrations.reverse()

try:
    with psycopg.connect(
        dbname = 'postgres',
        user = 'postgres',
        password = 'roma1234',
        host = 'localhost',
        port = '5432') as conn:
        logger.info('Connection to PostgreSQL DB successful')
        
        with conn.cursor() as cur:
            for file in migrations:
                path =f'{directory}{file}'
                print(path)

                with open(path, 'r') as command:
                    cur.execute(command.read())
                    logger.info('succes')
                    conn.commit()

except Exception as error:    
    logger.error(f"{error}")