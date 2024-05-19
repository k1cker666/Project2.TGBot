from enum import Enum, auto

import requests
from src.handlers.lesson_handler import LessonHandler
from src.handlers.repetition_handler import RepetitionHandler
from src.handlers.statistic_handler import StatisticHandler
from src.helpfuncs.menu import build_menu
from src.models.callback import CallbackData
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class StartHandler:

    name = "start"
    lesson_handler: LessonHandler
    repetition_handler: RepetitionHandler
    statistic_handler: StatisticHandler
    backend_url: str

    class CallBackType(Enum):
        auth = auto()

    def __init__(
        self,
        lesson_handler: LessonHandler,
        repetition_handler: RepetitionHandler,
        statistic_handler: StatisticHandler,
        backend_url: str,
    ):
        self.lesson_handler = lesson_handler
        self.repetition_handler = repetition_handler
        self.statistic_handler = statistic_handler
        self.backend_url = backend_url

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}, я бот, который поможет тебе выучить иностранные слова!"
        )
        user_token = self.__get_token(user.username)
        auth = self.__get_authorization_url(user_token)
        print(auth)
        buttons = [
            InlineKeyboardButton(
                "Авторизация",
                callback_data=CallbackData(
                    cb_processor=self.name, cb_type=self.CallBackType.auth.name
                ).to_string(),
            )
        ]
        reply_markup = InlineKeyboardMarkup(
            build_menu(buttons=buttons, n_cols=1)
        )
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Выбери действие",
            reply_markup=reply_markup,
        )

    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData,
    ):
        query = update.callback_query
        if callback_data.cb_type == self.CallBackType.auth.name:
            await query.delete_message()
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
                    "Посмотреть статистику",
                    callback_data=CallbackData(
                        cb_processor=self.statistic_handler.name,
                        cb_type=self.statistic_handler.CallBackType.init_stat.name,
                    ).to_string(),
                ),
            ]
            reply_markup = InlineKeyboardMarkup(build_menu(buttons, 2))
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Авторизация успешно выполнена\nВыбери следующее действие",
                reply_markup=reply_markup,
            )

    def __get_token(self, tg_login: str) -> str:
        r = requests.get(
            url=f"{self.backend_url}/get_token/", params={"tg_login": tg_login}
        )
        return r.json()["uuid_token"]

    def __get_authorization_url(self, uuid_token: str) -> str:
        r = requests.post(
            url=f"{self.backend_url}/authorization/",
            params={"uuid_token": uuid_token},
        )
        return r.text
