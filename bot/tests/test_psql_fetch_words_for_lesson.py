import pytest
from src.repository.word_repository import WordRepository


@pytest.mark.parametrize(
    "user_id, word_language, word_level, word_in_progress, res",
    [
        (1, "ru", "A1", 4, ["тест1", "тест2", "тест3", "тест4"]),
        (1, "en", "A1", 3, ["test2", "test3", "test4"]),
        (1, "en", "A1", 4, ["test2", "test3", "test4"]),
    ],
)
def test_fetch_words_for_lesson(
    psql_connect,
    setup_words_table,
    user_id,
    word_language,
    word_level,
    word_in_progress,
    res,
):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    lesson = word_repo.fetch_words_for_lesson(
        user_id, word_language, word_level, word_in_progress
    )
    words = [word.word for word in lesson]
    words.sort()
    assert words == res


@pytest.mark.parametrize(
    "user_id, word_language, word_level, word_in_progress, res",
    [(1, "en", "A2", 2, None), (1, "ru", "A2", 2, None)],
)
def test_fetch_words_for_lesson_nonetype(
    psql_connect,
    setup_words_table,
    user_id,
    word_language,
    word_level,
    word_in_progress,
    res,
):
    setup_words_table
    word_repo = WordRepository(psql_connect)
    words = word_repo.fetch_words_for_lesson(
        user_id, word_language, word_level, word_in_progress
    )
    assert words == res
