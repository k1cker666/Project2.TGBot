import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name='postgres', db_user='postgres', db_password='roma1234', db_host='localhost', db_port='5434'):
    connection = None
    try:
        connection = psycopg2.connect(
            database = db_name,
            user = db_user,
            password = db_password,
            host = db_host,
            port = db_port
        )
        print('Connection to PostgreSQL DB successful')
    except OperationalError as e:
        print(f'PostgreSQL: The error {e} occured')