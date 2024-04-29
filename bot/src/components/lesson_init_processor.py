from src.repository.word_repository import WordRepository
from src.repository.user_repository import UserRepository
from src.components.lesson_dto import LessonDTO, Question

class LessonInitProcessor:
    
    user_repository: UserRepository
    word_repository: WordRepository
    
    def __init__(self, user_repository, word_repository):
        self.user_repository = user_repository
        self.word_repository = word_repository
    
    def init(self) -> LessonDTO:
        questions = [
            Question(
                id = 1,
                word_to_translate = 'word_A',
                answers = ['A', 'B', 'C', 'D'],
                correct_answer = 'A'
            ),
            Question(
                id = 2,
                word_to_translate = 'word_B',
                answers = ['A', 'B', 'C', 'D'],
                correct_answer = 'B'
            )
        ]
        return LessonDTO(questions=questions)
    
    def init2(self, user_telegram_login: str):
        user = self.user_repository.fetch(user_telegram_login)
        words_in_lesson = user.words_in_lesson
