from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
    )
from telegram.ext import ContextTypes
from src.models.callback import CallbackData
from src.components.lesson_handler import LessonHandler
from src.components.repetition_handler import RepetitionHandler
from src.helpfuncs.menu import build_menu
from enum import Enum, auto

class StartHandler:
    
    name = "start"
    lesson_handler: LessonHandler
    repetition_handler: RepetitionHandler
    
    class CallBackType(Enum):
        auth = auto()
    
    def __init__(self, lesson_handler, repetition_handler):
        self.lesson_handler = lesson_handler
        self.repetition_handler = repetition_handler
    
    async def handle(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        ):
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}, я бот, который поможет тебе выучить иностранные слова!")
        buttons =[
            InlineKeyboardButton(
                "Авторизация",
                callback_data = CallbackData(
                        cb_processor = self.name,
                        cb_type = self.CallBackType.auth.name).to_string())
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
        callback_data: CallbackData
        ):
        query = update.callback_query
        if callback_data.cb_type == self.CallBackType.auth.name:
            await query.delete_message()
            buttons = [
                InlineKeyboardButton(
                    "Начать урок",
                    callback_data = CallbackData(
                        cb_processor = self.lesson_handler.name,
                        cb_type = self.lesson_handler.CallBackType.init_lesson.name).to_string()
                    ),
                InlineKeyboardButton(
                    "Посмотреть статистику",
                    url="https://www.google.ru/"
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