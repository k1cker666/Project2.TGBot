from src.db import psql, redis
from src.components.start_handler import StartHandler
from src.components.config import load_config, Config
from redis import Redis
from src.repository.word_repository import WordRepository
from src.repository.user_repository import UserRepository
from src.components.user_state_processor import UserStateProcessor

class Dependencies:

    redis_connect: Redis
    start_handler: StartHandler
    word_repository: WordRepository
    user_repository: UserRepository
    config: Config
    user_state_processor: UserStateProcessor
    
    def __init__(
        self,
        redis_connect,
        start_handler,
        word_repository,
        user_repository,
        config,
        user_state_processor
    ):
        self.redis_connect = redis_connect
        self.start_handler = start_handler
        self.word_repository = word_repository
        self.user_repository = user_repository
        self.config = config
        self.user_state_processor = user_state_processor
    
    def close(self):
        self.redis_connect.close()
        self.word_repository.connection.close()
        self.user_repository.connection.close()
        
class DependenciesBuilder:
    
    def build() -> Dependencies:
        config = load_config()
        psql_connect = psql.create_connection(config=config.psql)
        redis_connect = redis.create_connection(config=config.redis)
        start_handler = StartHandler()
        word_repository = WordRepository(connection=psql_connect)
        user_repository = UserRepository(connection=psql_connect)
        user_state_processor = UserStateProcessor(connection=redis_connect, config=config.redis)
        return Dependencies(
            redis_connect=redis_connect,
            start_handler=start_handler,
            word_repository=word_repository,
            user_repository=user_repository,
            config = config,
            user_state_processor = user_state_processor
        )