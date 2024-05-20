from enum import Enum, auto

from src.components.image_builder import ImageBuilder
from src.models.callback import CallbackData
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


class StatisticHandler:

    name = "statistic"
    user_repository: UserRepository
    word_repository: WordRepository
    image_builder: ImageBuilder
    common_word_count: int

    class CallBackType(Enum):
        init_stat = auto()

    def __init__(
        self,
        user_repository: UserRepository,
        word_repository: WordRepository,
        image_builder: ImageBuilder,
        common_word_count: int,
    ):
        self.user_repository = user_repository
        self.word_repository = word_repository
        self.image_builder = image_builder
        self.common_word_count = common_word_count

    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData,
    ):
        if callback_data.cb_type == self.CallBackType.init_stat.name:
            await self.send_statistic(update, context)

    async def send_statistic(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        user = self.user_repository.fetch_user_by_tg_login(
            tg_login=update.effective_user.username
        )
        passed_words = self.word_repository.fetch_count_passed_words(
            user_id=user.user_id, language_to_learn=user.language_to_learn
        )
        learned_words = self.word_repository.fetch_count_learned_words(
            user_id=user.user_id, language_to_learn=user.language_to_learn
        )
        photo_buffer = self.image_builder.get_progress_bar_image(
            passed_words=passed_words, learned_words=learned_words
        )
        caption = (
            f"Пользователь: <i>{user.tg_login}</i>"
            + f"\nАккаунт: <i>{user.login}</i>"
            + f"\nТекущий уровень изучаемых слов: <b>{user.word_level.get_description()}</b>"
            + f"\nПройдено слов: <b>{passed_words}/{self.common_word_count}</b>"
            + f"\nВыучено слов: <b>{learned_words}/{self.common_word_count}</b>"
        )
        query = update.callback_query
        await query.delete_message()
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_buffer,
            caption=caption,
            parse_mode=ParseMode.HTML,
        )
        photo_buffer.close()
