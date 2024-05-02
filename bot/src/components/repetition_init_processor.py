from bot.src.repository.user_repository import UserRepository
from bot.src.repository.wordinprogress_repository import WordInProgressRepository

class RepetitionInitProcessor:
    
    user_repository: UserRepository
    word_in_progress_repository: WordInProgressRepository
    
    def __init__(self, user_repository, word_in_progress_repository):
        self.user_repository = user_repository
        self.word_in_progress_repository = word_in_progress_repository