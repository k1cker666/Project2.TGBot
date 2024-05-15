import pytest
from src.repository.word_repository import WordRepository


@pytest.mark.parametrize(
    "word, language, res",
    [
        ("тест3", "ru", ["тест1", "тест2", "тест3", "тест4"]),
        ("тест1", "ru", ["тест1", "тест2", "тест3", "тест4"]),
        ("test1", "en", ["test1", "test2", "test3", "test4"]),
    ],
)
def test_fetch_words_for_answer(
    psql_connect, setup_words_table, word, language, res
):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    words = word_repo.fetch_words_for_answer(word, language)
    words.sort()
    words = [wordd.lower() for wordd in words]
    assert words == res
