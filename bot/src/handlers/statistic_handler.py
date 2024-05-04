from enum import Enum, auto
import os
from telegram import (
    Update
)
from telegram.ext import ContextTypes
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository
from src.components.image_builder import ImageBuilder
from src.models.callback import CallbackData

class StatisticHandler:
    
    name = "statistic"
    user_repository: UserRepository
    word_repository: WordRepository
    image_builder: ImageBuilder
    word_count: int
    
    class CallBackType(Enum):
        init_stat = auto()
        
    def __init__(
        self,
        user_repository: UserRepository,
        word_repository: WordRepository,
        image_builder: ImageBuilder,
        word_count: int
    ):
        self.user_repository = user_repository
        self.word_repository = word_repository
        self.image_builder = image_builder
        self.word_count = word_count
        
    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData
        ):
        query = update.callback_query
        if callback_data.cb_type == self.CallBackType.init_stat.name:
            await query.delete_message()
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=self.image_builder.get_progress_bar_image(),
                caption='Статистика'
            )
    
    async def send_statistic(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        ):
        user = self.user_repository.fetch_user_by_tg_login(tg_login="@k1cker666")
        learned_words = self.word_repository.fetch_count_learned_words(
            user_id=user.user_id,
            language_to_learn=user.language_to_learn
        )
        passed_words = self.word_repository.fetch_count_passed_words(
            user_id=user.user_id,
            language_to_learn=user.language_to_learn
        )