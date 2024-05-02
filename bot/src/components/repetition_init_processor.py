from src.components.lesson_dto import LessonDTO
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository

class RepetitionInitProcessor:
    
    user_repository: UserRepository
    word_repository: WordRepository
    
    def __init__(self, user_repository, word_repository):
        self.user_repository = user_repository
        self.word_repository = word_repository