from src import bot
from src.log import *
from src.db import psql, redis

def main():
    bot.start_bot()
    
def db_connect():
    psql.create_connection()
    redis.create_connectrion()

if __name__ == "__main__":
    db_connect()
    main()