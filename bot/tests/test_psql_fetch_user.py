import pytest
from src.repository.user_repository import UserRepository

@pytest.mark.parametrize(
    "id, res",
    [
        (1, '@k1cker666'),
        (1.0, '@k1cker666')
    ]
)
def test_fetch_user(psql_connect, setup_users_table, id, res):
    setup_users_table
    user_repo = UserRepository(psql_connect)
    assert user_repo.fetch(id).tg_login == res

@pytest.mark.parametrize(
    "id, res",
    [
        (0, None),
        (-10, None)
    ]
)
def test_fetch_nonetype(psql_connect, id, res):
    user_repo = UserRepository(psql_connect)
    assert user_repo.fetch(id) == res