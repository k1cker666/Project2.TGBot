from src import bot
from src.log import *
from src.dependencies import DependenciesBuilder
from psycopg2 import OperationalError
from redis.exceptions import ConnectionError

def main():
    try:
        dependencies = DependenciesBuilder.build()
    except OperationalError:
        logger.info('Application was not started')
        return
    except ConnectionError:
        logger.info('Application was not started')
        return
    else:
        bot.start_bot(dependencies)  

if __name__ == "__main__":
    main()