from enum import Enum, auto
from typing import List

from src.helpfuncs.menu import build_menu
from src.models.callback import CallbackData
from src.models.enums import WordLevel
from src.repository.user_repository import UserRepository
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


class SettingsHandler:

    name = "setting"
    user_repository: UserRepository

    class CallBackType(Enum):
        settings = auto()
        new_level_mes = auto()
        set_new_level = auto()

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData,
    ):
        if callback_data.cb_type == self.CallBackType.settings.name:
            await self.__send_settings_message(update, context)
        if callback_data.cb_type == self.CallBackType.new_level_mes.name:
            await self.__send_change_level_message(update, context)
        if callback_data.cb_type == self.CallBackType.set_new_level.name:
            await self.__set_new_level(
                update, context, callback_data.new_level
            )

    async def __send_settings_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        user = self.user_repository.fetch_user_by_tg_login(
            tg_login=update.effective_user.username
        )
        text = (
            f"Аккаунт: <i>{user.login}</i>"
            + f"\n\nОсновной язык: <b>{user.native_language.get_description()}</b>"
            + f"\nИзучаемый язык: <b>{user.language_to_learn.get_description()}</b>"
            + f"\n\nТекущий уровень слов: <b>{user.word_level.get_description()}</b>"
            + "\n\n<b>На данный момент нельзя сменить язык!(но когда-нибудь будет можно)</b>"
        )
        reply_markup = self.__build_settings_menu()
        query = update.callback_query
        await query.delete_message()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )

    async def __send_change_level_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        user = self.user_repository.fetch_user_by_tg_login(
            tg_login=update.effective_user.username
        )
        levels = {
            WordLevel.A1: [WordLevel.A2, WordLevel.A3],
            WordLevel.A2: [WordLevel.A1, WordLevel.A3],
            WordLevel.A3: [WordLevel.A1, WordLevel.A2],
        }
        new_levels = levels[user.word_level]
        text = "На какой уровень желаете перейти?"
        reply_markup = self.__build_new_level_menu(new_levels=new_levels)
        query = update.callback_query
        await query.delete_message()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=reply_markup,
        )

    async def __set_new_level(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        new_level: str,
    ):
        self.user_repository.update_user_word_level(
            word_level=new_level,
            tg_login=update.effective_user.username,
        )
        query = update.callback_query
        await query.delete_message()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Уровень успешно обновлен",
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(
                    text="Вернуться в меню",
                    callback_data=CallbackData(
                        cb_processor="start",
                        cb_type="menu",
                    ).to_string(),
                )
            ),
        )

    def __build_new_level_menu(self, new_levels: List[WordLevel]):
        buttons = []
        for level in new_levels:
            buttons.append(
                InlineKeyboardButton(
                    text=level.get_description(),
                    callback_data=CallbackData(
                        cb_processor=self.name,
                        cb_type=self.CallBackType.set_new_level.name,
                        new_level=level.name,
                    ).to_string(),
                )
            )
        footer_button = [
            InlineKeyboardButton(
                text="Вернуться в меню",
                callback_data=CallbackData(
                    cb_processor="start", cb_type="menu"
                ).to_string(),
            ),
        ]
        reply_markup = InlineKeyboardMarkup(
            build_menu(buttons=buttons, n_cols=2, footer_buttons=footer_button)
        )

        return reply_markup

    def __build_settings_menu(self):
        buttons = [
            InlineKeyboardButton(
                text="Поменять текущий уровень",
                callback_data=CallbackData(
                    cb_processor=self.name,
                    cb_type=self.CallBackType.new_level_mes.name,
                ).to_string(),
            ),
            InlineKeyboardButton(
                text="Вернуться в меню",
                callback_data=CallbackData(
                    cb_processor="start", cb_type="menu"
                ).to_string(),
            ),
        ]
        reply_markup = InlineKeyboardMarkup(
            build_menu(buttons=buttons, n_cols=1)
        )
        return reply_markup
