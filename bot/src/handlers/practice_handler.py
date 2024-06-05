from enum import Enum, auto
from typing import List

from src.components.image_builder import ImageBuilder
from src.components.practice_init_processor import PracticeInitProcessor
from src.components.user_state_processor import State, UserStateProcessor
from src.helpfuncs.menu import build_menu
from src.models.callback import CallbackData
from src.models.lesson_dto import LessonDTO, Question
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


class PracticeHandler:

    practice_init_processor: PracticeInitProcessor
    user_state_processor: UserStateProcessor
    image_builder: ImageBuilder
    user_repository: UserRepository
    word_repository: WordRepository
    name = "practice"

    class CallBackType(Enum):
        init_practice = auto()
        check_answer = auto()

    def __init__(
        self,
        practice_init_processor: PracticeInitProcessor,
        user_state_processor: UserStateProcessor,
        image_builder: ImageBuilder,
        user_repository: UserRepository,
        word_repository: WordRepository,
    ):
        self.practice_init_processor = practice_init_processor
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
        if callback_data.cb_type == self.CallBackType.init_practice.name:
            await self.__start_practice(update, context)
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

    async def __start_practice(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        query = update.callback_query
        await query.delete_message()
        data = self.practice_init_processor.get_lesson(
            user_telegram_login=update.effective_user.username
        )
        if data is None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Слов для практики пока нет!",
                reply_markup=InlineKeyboardMarkup.from_button(
                    InlineKeyboardButton(
                        text="Вернуться в меню",
                        callback_data=CallbackData(
                            cb_processor="menu", cb_type="base"
                        ).to_string(),
                    )
                ),
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

    async def __end_practice(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        questions: List[Question],
    ):
        query = update.callback_query
        await query.delete_message()
        photo_buffer = self.image_builder.get_end_lesson_image()
        summary = self.__get_word_summary(questions=questions)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_buffer,
            caption=summary,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(
                    text="Вернуться в меню",
                    callback_data=CallbackData(
                        cb_processor="menu", cb_type="base"
                    ).to_string(),
                )
            ),
        )
        photo_buffer.close()
        self.user_state_processor.set_state(
            user_id=update.effective_user.username,
            state=State.lesson_inactive,
        )

    def __get_word_summary(self, questions: List[Question]):
        summary = "Итак, подведем итоги. Слова из урока:\n"
        for question in questions:
            text = f"\n<b>{question['word_to_translate']} &#8212; {question['correct_answer']}</b>"
            summary += text
        return summary

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
        answers = data.questions[data.active_question]["answers"]
        if callback_data.word.lower() not in answers:
            query = update.callback_query
            await query.delete_message()
            return
        if callback_data.word.lower() != correct_answer:
            await self.__send_same_question(
                update=update, context=context, data=data
            )
            return
        if self.__have_next_question(data.active_question, data.questions):
            data = self.__update_active_question(
                user_id=update.effective_user.username, data=data
            )
            await self.__send_next_question(
                update=update, context=context, data=data
            )
        else:
            await self.__end_practice(
                update=update, context=context, questions=data.questions
            )
