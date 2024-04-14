import json
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
    )
from telegram.ext import ContextTypes
from src.helpfuncs.menu import build_menu
from enum import Enum, auto

class StartHandler:
    name = "start"
    
    class CallBackType(Enum):
        auth = auto()
        init_lesson = auto()
    
    async def handle(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        ):
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}, я бот, которы поможет тебе выучить иностранные слова!")
        buttons =[
            InlineKeyboardButton(
                "Авторизация",
                callback_data = json.dumps({
                    "cb_processor": self.name,
                    "cb_type": self.CallBackType.auth.value
                    })
                ),
            ]
        reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=1))
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Выбери действие",
            reply_markup=reply_markup
        )
        
    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        cb_type: str
        ):
        query = update.callback_query
        await query.answer()
        if cb_type == self.CallBackType.auth.value:
            query = update.callback_query
            await query.delete_message()
            buttons = [
                InlineKeyboardButton(
                    "Начать урок",
                    callback_data = json.dumps({
                        "cb_processor": "lesson",
                        "cb_type": self.CallBackType.init_lesson.value
                    })
                    ),
                InlineKeyboardButton(
                    "Посмотреть статистику",
                    callback_data = json.dumps({
                        "cb_processor": "stat"
                    })
                    )
            ]
            reply_markup = InlineKeyboardMarkup(
                build_menu(buttons, 1)
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Авторизация успешно выполнена\nВыбери следующее действие",
                reply_markup=reply_markup
            )