import pytest
from src.repository.word_repository import WordRepository

@pytest.mark.parametrize(
    "user_id, word_language, word_in_progress, res",
    [
        (1, 'en', 1, ['hello'])
    ]
)
def test_fetch_words_for_repetition(
    psql_connect,
    setup_words_table,
    user_id,
    word_language,
    word_in_progress,
    res
):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    words = word_repo.fetch_words_for_repetition(user_id, word_language, word_in_progress) 
    assert [word.word for word in words] == res

@pytest.mark.parametrize(
    "user_id, word_language, word_in_progress, res",
    [
        (2, 'en', 2, None)
    ]
)
def test_fetch_words_for_repetition_nonetype(
    psql_connect,
    setup_words_table,
    user_id,
    word_language,
    word_in_progress,
    res
):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    words = word_repo.fetch_words_for_repetition(user_id, word_language, word_in_progress) 
    assert words == res