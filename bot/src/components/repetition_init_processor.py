from typing import List
from src.models.user import User
from src.models.word import Word
from src.models.lesson_dto import LessonDTO, Question
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository

class RepetitionInitProcessor:
    
    user_repository: UserRepository
    word_repository: WordRepository
    
    def __init__(
        self,
        user_repository: UserRepository,
        word_repository: WordRepository
    ):
        self.user_repository = user_repository
        self.word_repository = word_repository
        
    def get_lesson(self, user_telegram_login: str) -> LessonDTO:
        user = self.user_repository.fetch_user_by_tg_login(user_telegram_login)
        words_for_lesson = self.word_repository.fetch_words_for_repetition(
            user_id=user.user_id,
            word_language=user.language_to_learn,
            words_in_lesson=user.words_in_lesson
        )
        
        return LessonDTO(questions=self.get_questions(
            user=user,
            words_for_lesson=words_for_lesson
        ))
    
    def get_questions(
        self,
        user: User,
        words_for_lesson: List[Word]
    ) -> List[Question]:
        questions = []
        for word in words_for_lesson:
            correct_answer = self.word_repository.fetch(
                id=word.word_id,
                language=user.native_language.name
            )
            questions.append(
                Question(
                    id=word.word_id,
                    word_to_translate=word.word,
                    answers=self.word_repository.fetch_words_for_answer(
                        word=correct_answer.word,
                        language=user.native_language.name),
                    correct_answer=correct_answer.word
                ))
        return questions