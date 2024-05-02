from enum import Enum, auto
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
    )
from telegram.ext import ContextTypes
from src.models.callback import CallbackData
from src.components.repetition_init_processor import RepetitionInitProcessor
from src.components.user_state_processor import UserStateProcessor

class RepetitionHandler:
    
    repetition_init_processor: RepetitionInitProcessor
    user_state_processor: UserStateProcessor
    name = "repetition"
    
    class CallBackType(Enum):
        init_repetition = auto()
        check_answer = auto()
        
    def __init__(
        self,
        repetition_init_processor: RepetitionInitProcessor,
        user_state_processor: UserStateProcessor
        ):
        self.repetition_init_processor = repetition_init_processor
        self.user_state_processor = user_state_processor
    
    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData
        ):
        if callback_data.cb_type == self.CallBackType.init_repetition.name:
            print('rep')