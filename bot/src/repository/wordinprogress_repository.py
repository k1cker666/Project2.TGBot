import psycopg

class WordInProgressRepository:
    
    connection: psycopg.Connection
    
    def __init__(
        self,
        connection: psycopg.Connection
        ):
        self.connection = connection