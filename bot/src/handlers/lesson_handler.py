from enum import Enum, auto
from typing import List, Literal

from src.components.image_builder import ImageBuilder
from src.components.lesson_init_processor import LessonInitProcessor
from src.components.user_state_processor import State, UserStateProcessor
from src.helpfuncs.menu import build_menu
from src.models.callback import CallbackData
from src.models.enums import WordLevel
from src.models.lesson_dto import LessonDTO, Question
from src.models.user import User
from src.repository.user_repository import UserRepository
from src.repository.word_repository import WordRepository
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


class LessonHandler:

    lesson_init_processor: LessonInitProcessor
    user_state_processor: UserStateProcessor
    image_builder: ImageBuilder
    user_repository: UserRepository
    word_repository: WordRepository
    name = "lesson"

    class CallBackType(Enum):
        init_lesson = auto()
        start_lesson = auto()
        check_answer = auto()
        del_summary = auto()

    def __init__(
        self,
        lesson_init_processor: LessonInitProcessor,
        user_state_processor: UserStateProcessor,
        image_builder: ImageBuilder,
        user_repository: UserRepository,
        word_repository: WordRepository,
    ):
        self.lesson_init_processor = lesson_init_processor
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
        if callback_data.cb_type == self.CallBackType.init_lesson.name:
            await self.__init_lesson(update, context)
        if callback_data.cb_type == self.CallBackType.start_lesson.name:
            await self.__start_lesson(update, context)
        if callback_data.cb_type == self.CallBackType.check_answer.name:
            await self.__check_answer(update, context, callback_data)
        if callback_data.cb_type == self.CallBackType.del_summary.name:
            await self.__del_summary(update, context)

    async def __del_summary(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        query = update.callback_query
        await query.delete_message()

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
            buttons.append(self.create_answer_button(word.capitalize()))
        reply_markup = InlineKeyboardMarkup(
            build_menu(buttons=buttons, n_cols=1)
        )
        return reply_markup

    async def __init_lesson(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        query = update.callback_query
        await query.delete_message()
        data = self.lesson_init_processor.get_lesson(
            user_telegram_login=update.effective_user.username
        )
        if data is None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Слова для изучения закончились!",
                reply_markup=InlineKeyboardMarkup.from_button(
                    InlineKeyboardButton(
                        text="Вернуться в меню",
                        callback_data=CallbackData(
                            cb_processor="menu", cb_type="base"
                        ).to_string(),
                    )
                ),
            )
            return
        self.user_state_processor.set_data(
            user_id=update.effective_user.username,
            data=data.model_dump_json(),
        )
        self.user_state_processor.set_state(
            user_id=update.effective_user.username,
            state=State.lesson_active,
        )
        text = self.__get_word_summary(questions=data.questions, type="start")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(
                    text="Начинаем",
                    callback_data=CallbackData(
                        cb_processor=self.name,
                        cb_type=self.CallBackType.start_lesson.name,
                    ).to_string(),
                )
            ),
        )

    def __get_new_message(self, original_message: str):
        text_lines = original_message.split("\n")
        modified_message = "\n".join(text_lines[2:])
        new_message = (
            f"<span class='tg-spoiler'>{modified_message}</span>"
            + "\n\nСлова скрыты под спойлер, пользуйся подсказкой только в крайнем случае!"
        )
        return new_message

    async def __start_lesson(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        query = update.callback_query
        new_message = self.__get_new_message(
            original_message=query.message.text
        )
        await query.edit_message_text(
            text=new_message,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(
                    text="Удалить данное сообщение",
                    callback_data=CallbackData(
                        cb_processor=self.name,
                        cb_type=self.CallBackType.del_summary.name,
                    ).to_string(),
                )
            ),
        )
        json_data = self.user_state_processor.get_data(
            user_id=update.effective_user.username
        )
        data = LessonDTO.model_validate_json(json_data)
        reply_markup = self.create_answers_menu(
            question=data.questions[data.active_question]
        )
        word_to_translate = data.questions[data.active_question][
            "word_to_translate"
        ].capitalize()
        photo_buffer = self.image_builder.get_start_image(word_to_translate)
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

    async def __end_lesson(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        is_level_empty: bool,
        questions: List[Question],
    ):
        query = update.callback_query
        await query.delete_message()
        photo_buffer = self.image_builder.get_end_lesson_image()
        summary = self.__get_word_summary(questions=questions, type="end")
        if is_level_empty:
            captions = {
                WordLevel.A1.name: "\n\nПоздравляю! Вы перешли на новый уровень слов: "
                + f"{WordLevel.A2.get_description()}",
                WordLevel.A2.name: "\n\nПоздравляю! Вы перешли на новый уровень слов: "
                + f"{WordLevel.A3.get_description()}",
                WordLevel.A3.name: "\n\nПоздравляю! Вы прошли все имеющиеся слова!",
            }
            user = self.user_repository.fetch_user_by_tg_login(
                tg_login=update.effective_user.username
            )
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo_buffer,
                caption=summary + captions[user.word_level.name],
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
            self.__update_user_word_level(user=user)
        else:
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
            user_id=update.effective_user.username, state=State.lesson_inactive
        )

    def __get_word_summary(
        self, questions: List[Question], type=Literal["start", "end"]
    ):
        summary_messages = {
            "start": "Запомни слова, которые нужно будет перевести:\n",
            "end": "Итак, подведем итоги. Слова из урока:\n",
        }
        summary = summary_messages[type]
        for question in questions:
            text = f"\n<b>{question['word_to_translate'].capitalize()} &#8212; {question['correct_answer']}</b>"
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
        self.__add_word_in_words_in_progress(
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
            await self.__end_lesson(
                update=update,
                context=context,
                is_level_empty=data.is_current_level_empty,
                questions=data.questions,
            )

    def __update_user_word_level(self, user: User):
        word_level = {
            WordLevel.A1.name: WordLevel.A2.name,
            WordLevel.A2.name: WordLevel.A3.name,
        }
        if user.word_level != WordLevel.A3:
            self.user_repository.update_user_word_level(
                user_id=user.user_id,
                word_level=word_level[user.word_level.name],
            )

    def __add_word_in_words_in_progress(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        data: LessonDTO,
    ):
        user = self.user_repository.fetch_user_by_tg_login(
            tg_login=update.effective_user.username
        )
        self.word_repository.add_word_in_words_in_progress(
            user_id=user.user_id,
            word_id=data.questions[data.active_question]["id"],
            language=user.language_to_learn,
        )
