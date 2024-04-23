import pytest
from src.components.user_state_processor import UserStateProcessor

@pytest.mark.parametrize(
    "x, y, res",
    [
        ("user1", {'test': 'test'}, {'test': 'test'}),
        ("user2", {'test1': 'test1', 'test2': 'test2'}, {'test1': 'test1', 'test2': 'test2'})
    ]
)
def test_get_data(redis_connect, config_init, x, y, res):
    user_state = UserStateProcessor(connection=redis_connect, config=config_init.redis)
    user_state.set_data(x, y, ttl = config_init.redis.ttl_for_test)
    assert user_state.get_data(x) == res

@pytest.mark.parametrize(
    "x, res",
    [
        ("user3", None)
    ]
)
def test_get_data_nonetype(redis_connect, config_init, x, res):
    user_state = UserStateProcessor(connection=redis_connect, config=config_init.redis)
    assert user_state.get_data(x) == res