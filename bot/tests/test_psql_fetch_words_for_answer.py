import pytest
from src.repository.word_repository import WordRepository

@pytest.mark.parametrize(
    "word, language, res",
    [
        ('видеть', 'ru', ['Видеть', 'Делать', 'Думать', 'Привет']),
        ('делать', 'ru', ['Видеть', 'Делать', 'Думать', 'Привет']),
        ('see', 'en', ['Do', 'Hello', 'See', 'Think'])
    ]
)
def test_fetch_words_for_answer(
    psql_connect,
    setup_words_table,
    word,
    language,
    res
):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    words = word_repo.fetch_words_for_answer(word, language)
    words.sort()
    assert words == res