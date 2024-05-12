from typing import List

from src.models.lesson_dto import LessonDTO, Question
from src.models.user import User
from src.models.word import Word
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository


class LessonInitProcessor:

    user_repository: UserRepository
    word_repository: WordRepository

    def __init__(
        self, user_repository: UserRepository, word_repository: WordRepository
    ):
        self.user_repository = user_repository
        self.word_repository = word_repository

    def get_lesson(self, user_telegram_login: str) -> LessonDTO:
        user = self.user_repository.fetch_user_by_tg_login(user_telegram_login)
        words_for_lesson = self.word_repository.fetch_words_for_lesson(
            user_id=user.user_id,
            word_language=user.language_to_learn,
            word_level=user.word_level,
            words_in_lesson=user.words_in_lesson,
        )
        count_words_in_current_level = (
            self.word_repository.fetch_count_words_in_current_level(
                user_id=user.user_id,
                word_language=user.language_to_learn,
                word_level=user.word_level,
            )
        )
        return (
            None
            if words_for_lesson is None
            else LessonDTO(
                questions=self.__get_questions(
                    user=user, words_for_lesson=words_for_lesson
                ),
                is_current_level_empty=self.__is_current_level_empty(
                    count_words_for_lesson=len(words_for_lesson),
                    count_words_in_current_level=count_words_in_current_level,
                ),
            )
        )

    def __get_questions(
        self, user: User, words_for_lesson: List[Word]
    ) -> List[Question]:
        questions = []
        for word in words_for_lesson:
            correct_answer = self.word_repository.fetch(
                id=word.word_id, language=user.native_language.name
            )
            questions.append(
                Question(
                    id=word.word_id,
                    word_to_translate=word.word,
                    answers=self.word_repository.fetch_words_for_answer(
                        word=correct_answer.word,
                        language=user.native_language.name,
                    ),
                    correct_answer=correct_answer.word,
                )
            )
        return questions

    def __is_current_level_empty(
        self, count_words_for_lesson: int, count_words_in_current_level: int
    ) -> bool:
        return count_words_in_current_level - count_words_for_lesson == 0
