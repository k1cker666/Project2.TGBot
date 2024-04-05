import psycopg
from psycopg import OperationalError
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_connection(db_name='testdb', db_user='postgres', db_password='roma1234', db_host='localhost', db_port='5432'): # db_host='localhost'/'postgres'
    
    connection = None
    try:
        connection = psycopg.connect(
            dbname = db_name,
            user = db_user,
            password = db_password,
            host = db_host,
            port = db_port
        )
        logger.info('Connection to PostgreSQL DB successful')
        return connection
    except OperationalError as e:
        logger.error(f'{e}')
        logger.info('Application was not started')
        raise OperationalError
    
def cheack_table(table_name, schema_name='tgbot'):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("""
            select exists (select *
            from information_schema.tables
            where table_name = %s
            and table_schema = %s) as table_exists;""",
            (table_name, schema_name))
        
        result = cur.fetchone()
        for res in result:
            return res
              
cheack_table('users', 'tgbot')