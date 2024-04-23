from enum import Enum, auto
import json
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes
from src.models.callback import WordCallback
from src.components.lesson_dto import LessonDTO
from src.helpfuncs.menu import build_menu
from src.components.user_state_processor import UserStateProcessor
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
        
        if cb_type == self.CallBackType.init_lesson.name:
            await query.delete_message()
            
            questions = self.lesson_init_processor.init()
            self.user_state_processor.set_data(user_id='kicker', data=questions.model_dump_json())
            
            buttons = []
            for word in questions.questions[questions.active_question]['answers']:
                buttons.append(self.create_answer_button(word))
            reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=1))
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Переведи слово {questions.questions[questions.active_question]['word_to_translate']}",
                reply_markup=reply_markup
            )
        
        if cb_type == self.CallBackType.check_answer.name:
            data = LessonDTO.model_validate_json(self.user_state_processor.get_data(user_id='kicker'))
            callback = WordCallback(*query.data.split(', '))
            if callback.word == data.questions[data.active_question]['correct_answer']:
                if data.active_question+1 != len(data.questions):
                    data.active_question +=1
                    self.user_state_processor.set_data(user_id='kicker', data=data.model_dump_json())
                    
                    buttons = []
                    for word in data.questions[data.active_question]['answers']:
                        buttons.append(self.create_answer_button(word))
                    reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=1))

                    await query.edit_message_text(f"Перевод верный\nСледующее слово {data.questions[data.active_question]['word_to_translate']}")
                    await query.edit_message_reply_markup(reply_markup)
                else:
                    await query.edit_message_text('Все слова урока переведены')
            else:
                buttons = []
                for word in data.questions[data.active_question]['answers']:
                    buttons.append(self.create_answer_button(word))
                reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=1))
                await query.edit_message_text(f"Перевод неверный.\nПопробуй еще раз перевести слово {data.questions[data.active_question]['word_to_translate']}")
                
                await query.edit_message_reply_markup(reply_markup)
                
            
    def create_answer_button(self, word: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=word,
            callback_data = f'{self.name}, {self.CallBackType.check_answer.name}, {word}'
            )