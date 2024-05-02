import pytest
from src.repository.word_repository import WordRepository

@pytest.mark.parametrize(
    "user_id, word_language, word_level, word_in_progress, res",
    [
        (1, 'en', 'A1', 2, ['do', 'think']),
        (1, 'ru', 'A1', 2, ['привет', 'делать']),
        (2, 'en', 'A1', 2, ['hello', 'do'])
    ]
)
def test_fetch_words_for_lesson(
    psql_connect,
    setup_words_table,
    user_id,
    word_language,
    word_level,
    word_in_progress,
    res
):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    words = word_repo.fetch_words_for_lesson(user_id, word_language, word_level, word_in_progress) 
    assert [word.word for word in words] == res

@pytest.mark.parametrize(
    "user_id, word_language, word_level, word_in_progress, res",
    [
        (1, 'en', 'A2', 2, None),
        (1, 'ru', 'A2', 2, None)
    ]
)
def test_fetch_words_for_lesson_nonetype(
    psql_connect,
    setup_words_table,
    user_id,
    word_language,
    word_level,
    word_in_progress,
    res
):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    words = word_repo.fetch_words_for_lesson(user_id, word_language, word_level, word_in_progress) 
    assert words == res