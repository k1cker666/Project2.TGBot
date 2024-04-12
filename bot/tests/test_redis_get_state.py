import pytest
from src.components.user_state_processor import State, UserStateProcessor

@pytest.mark.parametrize(
    "x, y, res",
    [
        ("user1", "lesson_active", "lesson_active"),
        ("user2", "lesson_inactive", "lesson_inactive")
    ]
)
def test_get_state(create_user_state_proc_obj: UserStateProcessor, x, y, res):
        user_state = create_user_state_proc_obj
        user_state.set_state(x, State[y])
        assert user_state.get_state(x) == res

@pytest.mark.parametrize(
    "x, res",
    [
        ("user3", None)
    ]
)
def test_get_state_nonetype(create_user_state_proc_obj: UserStateProcessor, x, res):
    user_state = create_user_state_proc_obj
    assert user_state.get_state(x) == res