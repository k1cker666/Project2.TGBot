import pytest
from src.db.psql import create_connection

@pytest.mark.parametrize(
    "id, res",
    [
        (0, None),
        (1, (1, 'ru', 'A1', 'привет')),
        ("2", (2, 'en', 'A1', 'hello')),
        (-3, None),
        (0.4, None)
    ]
)
def test_fetch(id, res):
    def fetch(id):
        with create_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "select * from words where word_id = %s",
                    (id,)
                )
                result = cur.fetchone()
                return result
    assert fetch(id) == res