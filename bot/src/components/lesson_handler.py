from enum import Enum, auto
import json
from telegram import (
    CallbackQuery,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes
from src.models.callback import CallbackData
from src.components.lesson_dto import LessonDTO, Question
from src.helpfuncs.menu import build_menu
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
        callback_data: CallbackData
        ):
        if callback_data.cb_type == self.CallBackType.init_lesson.name:
            await self.__start_lesson(update, context)
        if callback_data.cb_type == self.CallBackType.check_answer.name:
            await self.__check_answer(update, callback_data)
                
    def create_answer_button(self, word: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=word,
            callback_data=CallbackData(
                cb_processor=self.name,
                cb_type=self.CallBackType.check_answer.name,
                word=word
            ).to_string())
        
    def create_answers_menu(self, question: Question) -> InlineKeyboardMarkup:
        buttons = []
        for word in question['answers']:
            buttons.append(self.create_answer_button(word))
        reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=1))
        return reply_markup
        
    async def __start_lesson(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        ):
        query = update.callback_query
        await query.delete_message()
        data = self.lesson_init_processor.init()
        self.user_state_processor.set_data(user_id='kicker', data=data.model_dump_json())
        self.user_state_processor.set_state(user_id='kicker', state=State.lesson_active)
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Переведи слово {data.questions[data.active_question]['word_to_translate']}",
            reply_markup=reply_markup)
    
    async def __check_answer(self, update: Update, callback_data: CallbackData):
        data = LessonDTO.model_validate_json(self.user_state_processor.get_data(user_id='kicker'))
        if callback_data.word == data.questions[data.active_question]['correct_answer']:
            if self.__have_next_question(data.active_question, data.questions):
                data = self.__update_active_question(user_id='kicker', data=data)
                await self.__send_next_question(update=update, data=data)
            else:
                await self.__end_lesson(update=update, user_id='kicker')
        else:
            await self.__send_same_question(update=update, data=data)
            
    def __have_next_question(
        self,
        active_question: int,
        questions_pool: int
    ) -> bool:
        return active_question+1 != len(questions_pool)
    
    def __update_active_question(self, user_id: str, data: LessonDTO) -> LessonDTO:
        data.active_question +=1
        self.user_state_processor.set_data(user_id=user_id, data=data.model_dump_json())
        return data
    
    async def __send_next_question(self, update: Update, data: LessonDTO):
        query = update.callback_query
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        await query.edit_message_text(f"Перевод верный\nСледующее слово {data.questions[data.active_question]['word_to_translate']}")
        await query.edit_message_reply_markup(reply_markup)
        
    async def __end_lesson(self, update: Update, user_id:str):
        query = update.callback_query
        await query.edit_message_text('Все слова урока переведены')
        self.user_state_processor.set_state(user_id=user_id, state=State.lesson_inactive)
        
    async def __send_same_question(self, update: Update, data: LessonDTO):
        query = update.callback_query
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        await query.edit_message_text(f"Перевод неверный.\nПопробуй еще раз перевести слово {data.questions[data.active_question]['word_to_translate']}")
        await query.edit_message_reply_markup(reply_markup)