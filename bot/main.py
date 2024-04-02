from src import bot
from src.log import *
from src.dependencies import DependenciesBuilder
from psycopg2 import OperationalError
from redis.exceptions import ConnectionError

def main():
    try:
        deps = DependenciesBuilder.build()
        bot.start_bot(deps) 
    except OperationalError:
        return
    except ConnectionError:
        return

if __name__ == "__main__":
    main()