import psycopg
import pytest

@pytest.mark.parametrize(
    "table_name, schema_name, res",
    [
        ('users', 'public', True),
        ('words', 'public', True),
        ('words_in_progress', 'public', True),
        ('cities', 'public', False),
        ('users', 'other', False)
    ]
)
def test_check_psql_tables(table_name, schema_name, res):
    def check_psql_tables(table_name, schema_name):
        with psycopg.connect(
            dbname = 'tgbot',
            user = 'postgres',
            password = 'roma1234',
            host = 'localhost',
            port = '5432',
            autocommit = True) as conn:
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
    assert check_psql_tables(table_name, schema_name) == res