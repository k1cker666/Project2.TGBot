from enum import Enum, auto
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from telegram.ext import ContextTypes
from src.helpfuncs.menu import build_menu
from src.models.callback import Callback
from src.components.user_state_processor import UserStateProcessor, State
from src.components.lesson_init_processor import LessonInitProcessor

class LessonHandler:
    
    lesson_init_processor: LessonInitProcessor
    user_state_processor: UserStateProcessor
    name = "lesson"
    
    class CallBackType(Enum):
        init_lesson = auto()
    
    def __init__(
        self,
        lesson_init_processor: LessonInitProcessor,
        user_state_processor: UserStateProcessor
        ):
        self.lesson_init_processor = lesson_init_processor
        self.user_state_processor = user_state_processor
        
    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        cb_type: str
        ):
        query = update.callback_query
        await query.delete_message()
        if cb_type == self.CallBackType.init_lesson.name:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Начинаем урок"
            )
            words = self.lesson_init_processor.init()
            callback = Callback(
                cb_processor = self.name,
                cb_type = State.lesson_active.name,
                num_of_question = words.active_question,
                correct_answer = words.questions[0]["correct_answer"]
            )
            self.user_state_processor.set_data(user_id='kicker', data=callback)
            buttons = []
            for word in words.questions[0]["answers"]:
                buttons.append(self.create_answer_button(word))
            reply_markup = ReplyKeyboardMarkup(
                build_menu(buttons=buttons, n_cols=2),
                resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Переведи слово {words.questions[0]['word_to_translate']}",
                reply_markup=reply_markup
            )            
            
    def create_answer_button(self, word: str) -> KeyboardButton:
        return (KeyboardButton(word))