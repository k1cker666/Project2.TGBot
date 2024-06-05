from typing import Literal

from src.components.user_state_processor import State, UserStateProcessor
from src.handlers.lesson_handler import LessonHandler
from src.handlers.practice_handler import PracticeHandler
from src.handlers.repetition_handler import RepetitionHandler
from src.handlers.setting_handler import SettingsHandler
from src.handlers.statistic_handler import StatisticHandler
from src.helpfuncs.menu import build_menu
from src.models.callback import CallbackData
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class MenuBuilder:

    name = "menu"
    user_state_processor: UserStateProcessor
    lesson_handler: LessonHandler
    repetition_handler: RepetitionHandler
    practice_handler: PracticeHandler
    statistic_handler: StatisticHandler
    settings_handler: SettingsHandler

    def __init__(
        self,
        user_state_processor: UserStateProcessor,
        lesson_handler: LessonHandler,
        repetition_handler: RepetitionHandler,
        practice_handler: PracticeHandler,
        statistic_handler: StatisticHandler,
        settings_handler: SettingsHandler,
    ):
        self.user_state_processor = user_state_processor
        self.lesson_handler = lesson_handler
        self.repetition_handler = repetition_handler
        self.practice_handler = practice_handler
        self.statistic_handler = statistic_handler
        self.settings_handler = settings_handler

    async def build_base_menu(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        cb_type: Literal["base", "long_afk"],
    ):
        messages = {
            "base": "Главное меню\nЧто делаем дальше?",
            "long_afk": "Вы слишком долго бездействовали, урок закончился",
        }
        self.user_state_processor.set_state(
            user_id=update.effective_user.username, state=State.lesson_inactive
        )
        query = update.callback_query
        await query.delete_message()
        reply_markup = self.__reply_markup_for_authorized_user()
        await context.bot.send_message(
            text=messages[cb_type],
            chat_id=update.effective_chat.id,
            reply_markup=reply_markup,
        )

    def __reply_markup_for_authorized_user(self) -> InlineKeyboardMarkup:
        buttons = [
            InlineKeyboardButton(
                "Начать новый урок",
                callback_data=CallbackData(
                    cb_processor=self.lesson_handler.name,
                    cb_type=self.lesson_handler.CallBackType.init_lesson.name,
                ).to_string(),
            ),
            InlineKeyboardButton(
                "Повторить слова",
                callback_data=CallbackData(
                    cb_processor=self.repetition_handler.name,
                    cb_type=self.repetition_handler.CallBackType.init_repetition.name,
                ).to_string(),
            ),
            InlineKeyboardButton(
                "Практика",
                callback_data=CallbackData(
                    cb_processor=self.practice_handler.name,
                    cb_type=self.practice_handler.CallBackType.init_practice.name,
                ).to_string(),
            ),
        ]
        footer_button = [
            InlineKeyboardButton(
                "Посмотреть статистику",
                callback_data=CallbackData(
                    cb_processor=self.statistic_handler.name,
                    cb_type=self.statistic_handler.CallBackType.init_stat.name,
                ).to_string(),
            ),
            InlineKeyboardButton(
                "Настройки",
                callback_data=CallbackData(
                    cb_processor=self.settings_handler.name,
                    cb_type=self.settings_handler.CallBackType.settings.name,
                ).to_string(),
            ),
        ]
        reply_markup = InlineKeyboardMarkup(
            build_menu(
                buttons=buttons,
                n_cols=2,
                footer_buttons=footer_button,
            )
        )
        return reply_markup
