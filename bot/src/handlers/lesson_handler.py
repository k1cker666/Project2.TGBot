from enum import Enum, auto
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes
from src.components.lesson_init_processor import LessonInitProcessor
from src.components.user_state_processor import UserStateProcessor, State
from src.components.image_builder import ImageBuilder
from src.models.callback import CallbackData
from src.models.lesson_dto import LessonDTO, Question
from src.helpfuncs.menu import build_menu

class LessonHandler:
    
    lesson_init_processor: LessonInitProcessor
    user_state_processor: UserStateProcessor
    image_builder: ImageBuilder
    name = "lesson"
    
    class CallBackType(Enum):
        init_lesson = auto()
        check_answer = auto()
    
    def __init__(
        self,
        lesson_init_processor: LessonInitProcessor,
        user_state_processor: UserStateProcessor,
        image_builder: ImageBuilder
        ):
        self.lesson_init_processor = lesson_init_processor
        self.user_state_processor = user_state_processor
        self.image_builder = image_builder
        
    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData
        ):
        if callback_data.cb_type == self.CallBackType.init_lesson.name:
            await self.__start_lesson(update, context)
        if callback_data.cb_type == self.CallBackType.check_answer.name:
            await self.__check_answer(update, context, callback_data)
                
    def create_answer_button(self, word: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=word,
            callback_data=CallbackData(
                cb_processor = self.name,
                cb_type = self.CallBackType.check_answer.name,
                word=word).to_string())
        
    def create_answers_menu(self, question: Question) -> InlineKeyboardMarkup:
        buttons = []
        for word in question['answers']:
            buttons.append(self.create_answer_button(word))
        reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=1))
        return reply_markup
        
    async def __start_lesson(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.delete_message()
        data = self.lesson_init_processor.get_lesson(user_telegram_login='@k1cker666')
        self.user_state_processor.set_data(user_id=update.effective_user.username, data=data.model_dump_json())
        self.user_state_processor.set_state(user_id=update.effective_user.username, state=State.lesson_active)
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        photo_buffer = self.image_builder.get_start_image(data.questions[data.active_question]['word_to_translate'].capitalize())
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_buffer,
            reply_markup=reply_markup
        )
        photo_buffer.close()
    
    def __have_next_question(self, active_question: int, questions_pool: int) -> bool:
        return active_question+1 != len(questions_pool)
    
    def __update_active_question(self, user_id: str, data: LessonDTO) -> LessonDTO:
        data.active_question +=1
        self.user_state_processor.set_data(user_id=user_id, data=data.model_dump_json())
        return data
    
    async def __end_lesson(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.delete_message()
        photo_buffer = self.image_builder.get_end_lesson_image()
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_buffer
        )
        photo_buffer.close()
        self.user_state_processor.set_state(user_id=update.effective_user.username, state=State.lesson_inactive)
    
    async def __send_next_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: LessonDTO):
        query = update.callback_query
        await query.delete_message()
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        photo_buffer = self.image_builder.get_right_answer_image(data.questions[data.active_question]['word_to_translate'].capitalize())
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_buffer,
            reply_markup=reply_markup
        )
        photo_buffer.close()
        
    async def __send_same_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: LessonDTO):
        query = update.callback_query
        await query.delete_message()
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        photo_buffer = self.image_builder.get_wrong_answer_image(data.questions[data.active_question]['word_to_translate'].capitalize())
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_buffer,
            reply_markup=reply_markup
        )
        photo_buffer.close()
        
    async def __check_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: CallbackData):
        data = LessonDTO.model_validate_json(self.user_state_processor.get_data(user_id=update.effective_user.username))
        if callback_data.word.lower() == data.questions[data.active_question]['correct_answer']:
            if self.__have_next_question(data.active_question, data.questions):
                data = self.__update_active_question(user_id=update.effective_user.username, data=data)
                await self.__send_next_question(update=update, context=context, data=data)
            else:
                await self.__end_lesson(update=update, context=context)
        else:
            await self.__send_same_question(update=update, context=context, data=data)