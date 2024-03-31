from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup
    )
from telegram.ext import ContextTypes
from src.helpfuncs.menu import build_menu

class StartHandler:
    
    async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user_answer = query.data
        await query.answer()
        if str(user_answer) == "1":
            await query.edit_message_text("Авторизация успешно выполнена")
            buttons = [
                KeyboardButton("Начать урок"),
                KeyboardButton("Посмотреть статистику")
            ]
            reply_markup = ReplyKeyboardMarkup(build_menu(buttons, 2), resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Выбери действие",
                reply_markup=reply_markup
            )