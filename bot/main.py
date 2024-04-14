from src import bot
from src.dependencies import DependenciesBuilder
from psycopg import OperationalError
from redis.exceptions import ConnectionError
from loguru import logger

def main():
    try:
        deps = DependenciesBuilder.build()
        bot.start_bot(deps)
    except OperationalError:
        return
    except ConnectionError:
        return
    finally:    
        deps.close()
        logger.info("Application was stopped")
    
if __name__ == "__main__":
    main()