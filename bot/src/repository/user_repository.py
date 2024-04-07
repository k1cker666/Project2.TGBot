import psycopg

class UserRepository:
    
    connection: psycopg.Connection
    
    def __init__(self, connection):
        self.connection = connection