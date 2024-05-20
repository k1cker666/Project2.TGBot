from enum import Enum, auto
from typing import Literal

import requests
from src.components.user_state_processor import State, UserStateProcessor
from src.handlers.lesson_handler import LessonHandler
from src.handlers.repetition_handler import RepetitionHandler
from src.handlers.statistic_handler import StatisticHandler
from src.helpfuncs.menu import build_menu
from src.models.callback import CallbackData
from src.repository.user_repository import UserRepository
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class StartHandler:

    name = "start"
    lesson_handler: LessonHandler
    repetition_handler: RepetitionHandler
    statistic_handler: StatisticHandler
    backend_url: str
    user_repository: UserRepository
    user_state_processor: UserStateProcessor

    class CallBackType(Enum):
        auth = auto()
        menu = auto()

    def __init__(
        self,
        lesson_handler: LessonHandler,
        repetition_handler: RepetitionHandler,
        statistic_handler: StatisticHandler,
        backend_url: str,
        user_repository: UserRepository,
        user_state_processor: UserStateProcessor,
    ):
        self.lesson_handler = lesson_handler
        self.repetition_handler = repetition_handler
        self.statistic_handler = statistic_handler
        self.backend_url = backend_url
        self.user_repository = user_repository
        self.user_state_processor = user_state_processor

    def __get_authorization_url(self, uuid_token: str) -> str:
        return f"{self.backend_url}/authorization/?uuid_token={uuid_token}"

    def __check_user_authorization(self, tg_login):
        user = self.user_repository.fetch_user_by_tg_login(tg_login=tg_login)
        return bool(user)

    def __get_token(self, tg_login: str) -> str:
        r = requests.get(
            url=f"{self.backend_url}/get_token/", params={"tg_login": tg_login}
        )
        return r.json()["uuid_token"]

    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData,
    ):
        query = update.callback_query
        if callback_data.cb_type == self.CallBackType.auth.name:
            await query.delete_message()
            reply_markup = self.__reply_markup_for_authorized_user()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Авторизация успешно выполнена\nВыберите следующее действие",
                reply_markup=reply_markup,
            )

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if self.__check_user_authorization(tg_login=user.username):
            self.user_state_processor.set_state(
                user_id=user.username, state=State.lesson_inactive
            )
            reply_markup = self.__reply_markup_for_authorized_user()
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Вы уже авторизированы, выберите действие",
                reply_markup=reply_markup,
            )
        else:
            await update.message.reply_html(
                rf"Привет {user.mention_html()}, я бот, который поможет вам выучить иностранные слова!"
            )
            uuid_token = self.__get_token(tg_login=user.username)
            auth_url = self.__get_authorization_url(uuid_token=uuid_token)
            reply_markup = self.__reply_markup_for_authorization(
                auth_url=auth_url
            )
            await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="Выбери действие",
                reply_markup=reply_markup,
            )

    async def request_authorization(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        tg_login = update.effective_user.username
        uuid_token = self.__get_token(tg_login=tg_login)
        auth_url = self.__get_authorization_url(uuid_token=uuid_token)
        reply_markup = self.__reply_markup_for_authorization(auth_url=auth_url)
        query = update.callback_query
        await query.delete_message()
        await context.bot.send_message(
            text="Сначала обходимо пройти авторизацию",
            chat_id=update.effective_chat.id,
            reply_markup=reply_markup,
        )

    async def build_base_menu(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        type: Literal["menu", "long_afk"] = "menu",
    ):
        messages = {
            "menu": "Главное меню\nЧто делаем дальше?",
            "long_afk": "Вы слишком долго бездействовали, урок закончился",
        }
        query = update.callback_query
        await query.delete_message()
        reply_markup = self.__reply_markup_for_authorized_user()
        await context.bot.send_message(
            text=messages[type],
            chat_id=update.effective_chat.id,
            reply_markup=reply_markup,
        )

    def __reply_markup_for_authorization(
        self, auth_url: str
    ) -> InlineKeyboardMarkup:
        buttons = [
            InlineKeyboardButton(
                text="Авторизация",
                url=auth_url,
            ),
            InlineKeyboardButton(
                text="Проверить авторизацию",
                callback_data=CallbackData(
                    cb_processor=self.name,
                    cb_type=self.CallBackType.auth.name,
                ).to_string(),
            ),
        ]
        reply_markup = InlineKeyboardMarkup(
            build_menu(buttons=buttons, n_cols=1)
        )
        return reply_markup

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
                "Посмотреть статистику",
                callback_data=CallbackData(
                    cb_processor=self.statistic_handler.name,
                    cb_type=self.statistic_handler.CallBackType.init_stat.name,
                ).to_string(),
            ),
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(buttons, 2))
        return reply_markup
