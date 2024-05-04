from enum import Enum, auto
from telegram import (
    Update
)
from telegram.ext import ContextTypes
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository
from src.models.callback import CallbackData

class StatisticHandler:
    
    name = "statistic"
    user_repository: UserRepository
    word_repository: WordRepository
    
    class CallBackType(Enum):
        init_stat = auto()
        
    def __init__(
        self,
        user_repository: UserRepository,
        word_repository: WordRepository
    ):
        self.user_repository = user_repository
        self.word_repository = word_repository
        
    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData
        ):
        query = update.callback_query
        if callback_data.cb_type == self.CallBackType.init_stat.name:
            await query.delete_message()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Статистика'
            )