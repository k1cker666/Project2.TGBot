import pytest
from src.repository.user_repository import UserRepository

@pytest.mark.parametrize(
    "tg_login, res",
    [
        ('@k1cker666', 1)
    ]
)
def test_fetch_user_by_tg_login(psql_connect, setup_users_table, tg_login, res):
    setup_users_table
    user_repo = UserRepository(psql_connect)
    assert user_repo.fetch_user_by_tg_login(tg_login).user_id == res

@pytest.mark.parametrize(
    "id, res",
    [
        ('', None)
    ]
)
def test_fetch_nonetype_by_tg_login(psql_connect, id, res):
    user_repo = UserRepository(psql_connect)
    assert user_repo.fetch_user_by_tg_login(id) == res