import pytest
from src.repository.user_repository import UserRepository

@pytest.mark.parametrize(
    "id, res",
    [
        (32766, '@test'),
        (32766.0, '@test')
    ]
)
def test_fetch_user_by_id(psql_connect, setup_users_table, id, res):
    setup_users_table
    user_repo = UserRepository(psql_connect)
    assert user_repo.fetch_user_by_id(id).tg_login == res

@pytest.mark.parametrize(
    "id, res",
    [
        (32767, None),
        (-10, None)
    ]
)
def test_fetch_nonetype_by_id(psql_connect, id, res):
    user_repo = UserRepository(psql_connect)
    assert user_repo.fetch_user_by_id(id) == res