import pytest
from src.db.psql import create_connection

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
def test_cheack_psql_tables(table_name, schema_name, res):
    def cheack_psql_tables(table_name, schema_name):
        with create_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select exists (select *
                    from information_schema.tables
                    where table_name = %s
                    and table_schema = %s) as table_exists;""",
                    (table_name, schema_name))

                result = cur.fetchone()
                for res in result:
                    return res
    assert cheack_psql_tables(table_name, schema_name) == res
                