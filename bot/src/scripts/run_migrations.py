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
        dbname = 'postgres',
        user = 'postgres',
        password = 'roma1234',
        host = 'localhost',
        port = '5432') as conn:
        logger.info('Connection to PostgreSQL DB successful')
        
        with conn.cursor() as cur:
            for file in migrations:
                path =f'{directory}{file}'

                with open(path, 'r') as command:
                    cur.execute(command.read())
                    conn.commit()
                    logger.info(f'Migration {file} complete')

except Exception as error:    
    logger.error(f"{error}")