from psycopg import OperationalError
from redis.exceptions import ConnectionError
from src import bot
from src.dependencies import DependenciesBuilder
from src.log import logger_config, logger_httpx, logger_main


logger_config
logger_httpx
logger_main


def main():
    try:
        deps = DependenciesBuilder.build()
        bot.start_bot(deps)
        deps.close()
    except OperationalError:
        return
    except ConnectionError:
        return


if __name__ == "__main__":
    main()
