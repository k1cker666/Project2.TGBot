import pytest
from src.db.psql import cheack_table

@pytest.mark.parametrize(
    "table_name, schema_name, res",
    [
        ('users', 'tgbot', True),
        ('words', 'tgbot', True),
        ('words_in_progress', 'tgbot', True),
        ('cities', 'tgbot', False),
        ('users', 'public', False)
    ]
)
def test_db(table_name, schema_name, res):
    assert cheack_table(table_name, schema_name) == res