import pytest
import redis
from src.components.user_state_processor import UserStateProcessor
from src.components.config import load_config

@pytest.fixture(scope="session")
def create_user_state_obj():
    config = load_config().redis
    with redis.Redis(
        host = config.host,
        port = config.port,
        decode_responses = True,
        encoding = "utf-8") as conn:
        user_state = UserStateProcessor(connection=conn, config=config)
        print("Вызов")
        return user_state