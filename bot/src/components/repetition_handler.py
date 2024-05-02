from enum import Enum, auto
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
    )
from telegram.ext import ContextTypes
from src.components.lesson_dto import LessonDTO, Question
from src.helpfuncs.menu import build_menu
from src.models.callback import CallbackData
from src.components.repetition_init_processor import RepetitionInitProcessor
from src.components.user_state_processor import State, UserStateProcessor

class RepetitionHandler:
    
    repetition_init_processor: RepetitionInitProcessor
    user_state_processor: UserStateProcessor
    name = "repetition"
    
    class CallBackType(Enum):
        init_repetition = auto()
        check_answer = auto()
        
    def __init__(
        self,
        repetition_init_processor: RepetitionInitProcessor,
        user_state_processor: UserStateProcessor
        ):
        self.repetition_init_processor = repetition_init_processor
        self.user_state_processor = user_state_processor
    
    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData
        ):
        if callback_data.cb_type == self.CallBackType.init_repetition.name:
            await self.__start_repetition(update, context)
        if callback_data.cb_type == self.CallBackType.check_answer.name:
            await self.__check_answer(update, callback_data)
                
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
        
    async def __start_repetition(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.delete_message()
        data = self.repetition_init_processor.get_lesson(user_telegram_login='@k1cker666')
        self.user_state_processor.set_data(user_id=update.effective_user.username, data=data.model_dump_json())
        self.user_state_processor.set_state(user_id=update.effective_user.username, state=State.lesson_active)
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Переведи слово {data.questions[data.active_question]['word_to_translate'].capitalize()}",
            reply_markup=reply_markup)
    
    def __have_next_question(self, active_question: int, questions_pool: int) -> bool:
        return active_question+1 != len(questions_pool)
    
    def __update_active_question(self, user_id: str, data: LessonDTO) -> LessonDTO:
        data.active_question +=1
        self.user_state_processor.set_data(user_id=user_id, data=data.model_dump_json())
        return data
    
    async def __end_repetition(self, update: Update):
        query = update.callback_query
        await query.edit_message_text('Больше нет слов для перевода')
        self.user_state_processor.set_state(user_id=update.effective_user.username, state=State.lesson_inactive)
    
    async def __send_next_question(self, update: Update, data: LessonDTO):
        query = update.callback_query
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        await query.edit_message_text(f"Перевод верный\nСледующее слово {data.questions[data.active_question]['word_to_translate'].capitalize()}")
        await query.edit_message_reply_markup(reply_markup)
    
    async def __send_same_question(self, update: Update, data: LessonDTO):
        query = update.callback_query
        reply_markup = self.create_answers_menu(question=data.questions[data.active_question])
        await query.edit_message_text(f"Перевод неверный.\nПопробуй еще раз перевести слово {data.questions[data.active_question]['word_to_translate'].capitalize()}")
        await query.edit_message_reply_markup(reply_markup)
    
    async def __check_answer(self, update: Update, callback_data: CallbackData):
        data = LessonDTO.model_validate_json(self.user_state_processor.get_data(user_id=update.effective_user.username))
        if callback_data.word.lower() == data.questions[data.active_question]['correct_answer']:
            if self.__have_next_question(data.active_question, data.questions):
                data = self.__update_active_question(user_id=update.effective_user.username, data=data)
                await self.__send_next_question(update=update, data=data)
            else:
                await self.__end_repetition(update=update)
        else:
            await self.__send_same_question(update=update, data=data)