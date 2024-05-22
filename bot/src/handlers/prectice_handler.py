from enum import Enum, auto

from src.components.image_builder import ImageBuilder
from src.components.practice_init_processor import PracticeInitProcessor
from src.components.user_state_processor import UserStateProcessor
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository


class PracticeHandler:

    practice_init_processor: PracticeInitProcessor
    user_state_processor: UserStateProcessor
    image_builder: ImageBuilder
    user_repository: UserRepository
    word_repository: WordRepository
    name = "practice"

    class CallBackType(Enum):
        init_prictice = auto()
        check_answer = auto()

    def __init__(
        self,
        prictice_init_processor: PracticeInitProcessor,
        user_state_processor: UserStateProcessor,
        image_builder: ImageBuilder,
        user_repository: UserRepository,
        word_repository: WordRepository,
    ):
        self.prictice_init_processor = prictice_init_processor
        self.user_state_processor = user_state_processor
        self.image_builder = image_builder
        self.user_repository = user_repository
        self.word_repository = word_repository
