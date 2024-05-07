import pytest
from src.repository.word_repository import WordRepository

@pytest.mark.parametrize(
    "id, language, res",
    [
        (-1, 'en', 'test1'),
        (-1, 'ru', 'тест1'),
        ("-1", 'ru', 'тест1')
    ]
)
def test_fetch_word(psql_connect, setup_words_table, id, language, res):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    assert word_repo.fetch(id, language).word == res

@pytest.mark.parametrize(
    "id, language, res",
    [
        (0, 'en', None),
        (-100, 'ru', None),
        ("-10", 'ru', None)
    ]
)
def test_fetch_nonetype(psql_connect, id, language, res):
    word_repo = WordRepository(psql_connect)
    assert word_repo.fetch(id, language) == res