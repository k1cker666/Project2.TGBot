from enum import Enum, auto

from src.components.image_builder import ImageBuilder
from src.components.repetition_init_processor import RepetitionInitProcessor
from src.components.user_state_processor import State, UserStateProcessor
from src.helpfuncs.menu import build_menu
from src.models.callback import CallbackData
from src.models.lesson_dto import LessonDTO, Question
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class RepetitionHandler:  # TODO 2)сообщение пользователю если он изучил все слова

    repetition_init_processor: RepetitionInitProcessor
    user_state_processor: UserStateProcessor
    image_builder: ImageBuilder
    user_repository: UserRepository
    word_repository: WordRepository
    name = "repetition"

    class CallBackType(Enum):
        init_repetition = auto()
        check_answer = auto()

    def __init__(
        self,
        repetition_init_processor: RepetitionInitProcessor,
        user_state_processor: UserStateProcessor,
        image_builder: ImageBuilder,
        user_repository: UserRepository,
        word_repository: WordRepository,
    ):
        self.repetition_init_processor = repetition_init_processor
        self.user_state_processor = user_state_processor
        self.image_builder = image_builder
        self.user_repository = user_repository
        self.word_repository = word_repository

    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData,
    ):
        if callback_data.cb_type == self.CallBackType.init_repetition.name:
            await self.__start_repetition(update, context)
        if callback_data.cb_type == self.CallBackType.check_answer.name:
            await self.__check_answer(
                update, context=context, callback_data=callback_data
            )

    def create_answer_button(self, word: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=word,
            callback_data=CallbackData(
                cb_processor=self.name,
                cb_type=self.CallBackType.check_answer.name,
                word=word,
            ).to_string(),
        )

    def create_answers_menu(self, question: Question) -> InlineKeyboardMarkup:
        buttons = []
        for word in question["answers"]:
            buttons.append(self.create_answer_button(word))
        reply_markup = InlineKeyboardMarkup(
            build_menu(buttons=buttons, n_cols=1)
        )
        return reply_markup

    async def __start_repetition(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        query = update.callback_query
        await query.delete_message()
        data = self.repetition_init_processor.get_lesson(
            user_telegram_login=update.effective_user.username
        )
        if data is None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Слов для повторения пока нет!",
            )
        else:
            self.user_state_processor.set_data(
                user_id=update.effective_user.username,
                data=data.model_dump_json(),
            )
            self.user_state_processor.set_state(
                user_id=update.effective_user.username,
                state=State.lesson_active,
            )
            reply_markup = self.create_answers_menu(
                question=data.questions[data.active_question]
            )
            word_to_translate = data.questions[data.active_question][
                "word_to_translate"
            ].capitalize()
            photo_buffer = self.image_builder.get_start_image(
                word_to_translate
            )
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo_buffer,
                reply_markup=reply_markup,
            )
            photo_buffer.close()

    def __have_next_question(
        self, active_question: int, questions_pool: int
    ) -> bool:
        return active_question + 1 != len(questions_pool)

    def __update_active_question(
        self, user_id: str, data: LessonDTO
    ) -> LessonDTO:
        data.active_question += 1
        self.user_state_processor.set_data(
            user_id=user_id, data=data.model_dump_json()
        )
        return data

    async def __end_repetition(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):
        query = update.callback_query
        await query.delete_message()
        photo_buffer = self.image_builder.get_end_lesson_image()
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo_buffer
        )
        photo_buffer.close()
        self.user_state_processor.set_state(
            user_id=update.effective_user.username,
            state=State.lesson_inactive,
        )

    async def __send_next_question(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        data: LessonDTO,
    ):
        query = update.callback_query
        await query.delete_message()
        reply_markup = self.create_answers_menu(
            question=data.questions[data.active_question]
        )
        word_to_translate = data.questions[data.active_question][
            "word_to_translate"
        ].capitalize()
        photo_buffer = self.image_builder.get_right_answer_image(
            word_to_translate
        )
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_buffer,
            reply_markup=reply_markup,
        )
        photo_buffer.close()

    async def __send_same_question(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        data: LessonDTO,
    ):
        query = update.callback_query
        await query.delete_message()
        reply_markup = self.create_answers_menu(
            question=data.questions[data.active_question]
        )
        word_to_translate = data.questions[data.active_question][
            "word_to_translate"
        ].capitalize()
        photo_buffer = self.image_builder.get_wrong_answer_image(
            word_to_translate
        )
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_buffer,
            reply_markup=reply_markup,
        )
        photo_buffer.close()

    async def __check_answer(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        callback_data: CallbackData,
    ):
        json_data = self.user_state_processor.get_data(
            user_id=update.effective_user.username
        )
        data = LessonDTO.model_validate_json(json_data)
        correct_answer = data.questions[data.active_question]["correct_answer"]
        if callback_data.word.lower() == correct_answer:
            self.__decrease_numder_of_repetitions(
                update=update, context=context, data=data
            )
            if self.__have_next_question(data.active_question, data.questions):
                data = self.__update_active_question(
                    user_id=update.effective_user.username, data=data
                )
                await self.__send_next_question(
                    update=update, context=context, data=data
                )
            else:
                await self.__end_repetition(
                    update=update,
                    context=context,
                )
        else:
            await self.__send_same_question(
                update=update, context=context, data=data
            )

    def __decrease_numder_of_repetitions(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        data: LessonDTO,
    ):
        user = self.user_repository.fetch_user_by_tg_login(
            tg_login=update.effective_user.username
        )
        self.word_repository.decrease_numder_of_repetitions(
            user_id=user.user_id,
            word_id=data.questions[data.active_question]["id"],
            language=user.language_to_learn,
        )
