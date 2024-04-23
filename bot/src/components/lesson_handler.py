from enum import Enum, auto
import json
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes
from src.helpfuncs.menu import build_menu
from src.models.callback import Data
from src.components.user_state_processor import UserStateProcessor, State
from src.components.lesson_init_processor import LessonInitProcessor

class LessonHandler:
    
    lesson_init_processor: LessonInitProcessor
    user_state_processor: UserStateProcessor
    name = "lesson"
    
    class CallBackType(Enum):
        init_lesson = auto()
        check_answer = auto()
    
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
            words = self.lesson_init_processor.init()
            data = Data(
                state = State.lesson_active.name,
                num_of_question = words.active_question,
                correct_answer = words.questions[words.active_question]["correct_answer"]
            )
            self.user_state_processor.set_data(user_id='kicker', data=data)
            buttons = []
            for word in words.questions[data["num_of_question"]]["answers"]:
                buttons.append(self.create_answer_button(word))
            reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=1))
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Переведи слово {words.questions[0]['word_to_translate']}",
                reply_markup=reply_markup
            )
            
    def create_answer_button(self, word: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=word,
            callback_data = f'{self.name}, {self.CallBackType.check_answer.name}, {word}'
            )