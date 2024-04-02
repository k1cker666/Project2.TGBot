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
    
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}, я бот, которы поможет тебе выучить иностранные слова!")
        buttons =[
            InlineKeyboardButton(
                "Авторизация",
                callback_data = str({
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
        
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, cb_type):
        query = update.callback_query
        await query.answer()
        if cb_type == self.CallBackType.auth.value:
            query = update.callback_query
            await query.delete_message()
            buttons = [
                KeyboardButton("Начать урок"),
                KeyboardButton("Посмотреть статистику")
            ]
            reply_markup = ReplyKeyboardMarkup(build_menu(buttons, 2), resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Авторизация успешно выполнена\nВыбери следующее действие",
                reply_markup=reply_markup
            )