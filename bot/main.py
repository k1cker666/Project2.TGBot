from pprint import pprint
from src import bot
from src.dependencies import DependenciesBuilder
from psycopg import OperationalError
from redis.exceptions import ConnectionError

def main():
    try:
        deps = DependenciesBuilder.build()
        
        print(deps.user_state_processor.get_state('privet'))
        
        bot.start_bot(deps)
        deps.close()
    except OperationalError:
        return
    except ConnectionError:
        return

if __name__ == "__main__":
    main()