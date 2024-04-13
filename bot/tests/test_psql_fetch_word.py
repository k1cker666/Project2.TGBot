import pytest
from src.repository.word_repository import WordRepository

@pytest.mark.parametrize(
    "id, language, res",
    [
        (1, 'en', 'hello'),
        (1, 'ru', 'привет'),
        ("1", 'ru', 'привет')
    ]
)
def test_fetch_word(create_psql_connect, setup_words_table, id, language, res):
    conn = create_psql_connect
    setup_words_table
    word_repo = WordRepository(conn)
    assert word_repo.fetch(id, language).word == res

@pytest.mark.parametrize(
    "id, language, res",
    [
        (0, 'en', None),
        (100, 'ru', None),
        ("10", 'ru', None)
    ]
)
def test_fetch_nonetype(create_psql_connect, id, language, res):
    conn = create_psql_connect
    word_repo = WordRepository(conn)
    assert word_repo.fetch(id, language) == res