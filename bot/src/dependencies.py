from src.db import psql, redis
from src.components.config import load_config, EnvConfig
from src.components.lesson_init_processor import LessonInitProcessor
from src.components.user_state_processor import UserStateProcessor
from src.components.repetition_init_processor import RepetitionInitProcessor
from src.components.image_builder import ImageBuilder
from src.handlers.start_handler import StartHandler
from src.handlers.repetition_handler import RepetitionHandler
from src.handlers.lesson_handler import LessonHandler
from src.handlers.statistic_handler import StatisticHandler
from src.repository.word_repository import WordRepository
from src.repository.user_repository import UserRepository
from loguru import logger

class Dependencies:

    start_handler: StartHandler
    word_repository: WordRepository
    user_repository: UserRepository
    config: EnvConfig
    user_state_processor: UserStateProcessor
    
    def __init__(
        self,
        start_handler: StartHandler,
        word_repository: WordRepository,
        user_repository: UserRepository,
        config: EnvConfig,
        user_state_processor: UserStateProcessor,
        lesson_handler: LessonHandler,
        repetition_handler: RepetitionHandler,
        statistic_handler: StatisticHandler
    ):
        self.start_handler = start_handler
        self.word_repository = word_repository
        self.user_repository = user_repository
        self.config = config
        self.user_state_processor = user_state_processor
        self.lesson_handler = lesson_handler
        self.repetition_handler = repetition_handler
        self.statistic_handler = statistic_handler
    
    def close(self):
        self.user_state_processor.conn.close()
        logger.info("Redis connections closed")
        self.word_repository.connection_pool.close()
        self.user_repository.connection_pool.close()
        logger.info("PostgreSQL connections closed")
        
class DependenciesBuilder:
    
    def build() -> Dependencies:
        config = load_config()
        psql_connect_pool = psql.create_connection_pool(config=config.psql)
        redis_connect = redis.create_connection(config=config.redis)
        
        word_repository = WordRepository(connection_pool=psql_connect_pool)
        user_repository = UserRepository(connection_pool=psql_connect_pool)
        
        image_builder = ImageBuilder(
            common_word_count=config.common_word_count
        )
        
        user_state_processor = UserStateProcessor(
            connection=redis_connect,
            config=config.redis
        )
        
        lesson_init_processor = LessonInitProcessor(
            user_repository=user_repository,
            word_repository=word_repository
        )
        lesson_handler = LessonHandler(
            lesson_init_processor=lesson_init_processor,
            user_state_processor=user_state_processor,
            image_builder=image_builder,
            user_repository=user_repository
        )
        
        repetition_init_processor = RepetitionInitProcessor(
            user_repository=user_repository,
            word_repository=word_repository
        )
        repetition_handler = RepetitionHandler(
            repetition_init_processor=repetition_init_processor,
            user_state_processor=user_state_processor,
            image_builder=image_builder
        )
        
        statistic_handler = StatisticHandler(
            user_repository=user_repository,
            word_repository=word_repository,
            image_builder=image_builder,
            common_word_count=config.common_word_count
        )
        
        start_handler = StartHandler(
            lesson_handler=lesson_handler,
            repetition_handler=repetition_handler,
            statistic_handler=statistic_handler
        )
        
        return Dependencies(
            start_handler=start_handler,
            word_repository=word_repository,
            user_repository=user_repository,
            config = config,
            user_state_processor = user_state_processor,
            lesson_handler = lesson_handler,
            repetition_handler = repetition_handler,
            statistic_handler = statistic_handler
        )