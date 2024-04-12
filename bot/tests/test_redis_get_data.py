import pytest
from src.components.user_state_processor import UserStateProcessor

@pytest.mark.parametrize(
    "x, y, res",
    [
        ("user1", {'test': 'test'}, {'test': 'test'}),
        ("user2", {'test1': 'test1', 'test2': 'test2'}, {'test1': 'test1', 'test2': 'test2'})
    ]
)
def test_get_data(create_user_state_proc_obj: UserStateProcessor, x, y, res):
        user_state = create_user_state_proc_obj
        user_state.set_data(x, y)
        assert user_state.get_data(x) == res

@pytest.mark.parametrize(
    "x, res",
    [
        ("user3", None)
    ]
)
def test_get_data_nonetype(create_user_state_proc_obj: UserStateProcessor, x, res):
    user_state = create_user_state_proc_obj
    assert user_state.get_data(x) == res