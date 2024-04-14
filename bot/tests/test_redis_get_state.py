import pytest
from src.components.user_state_processor import State, UserStateProcessor

@pytest.mark.parametrize(
    "x, y, res",
    [
        ("user1", "lesson_active", "lesson_active"),
        ("user2", "lesson_inactive", "lesson_inactive")
    ]
)
def test_get_state(redis_connect, config_init, x, y, res):
    user_state = UserStateProcessor(connection=redis_connect, config=config_init.redis)
    user_state.set_state(x, State[y])
    assert user_state.get_state(x) == res

@pytest.mark.parametrize(
    "x, res",
    [
        ("user3", None)
    ]
)
def test_get_state_nonetype(redis_connect, config_init, x, res):
    user_state = UserStateProcessor(connection=redis_connect, config=config_init.redis)
    assert user_state.get_state(x) == res