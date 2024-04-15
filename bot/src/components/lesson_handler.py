from enum import Enum, auto
from telegram import (
    Update
)
from telegram.ext import ContextTypes
from src.components.lesson_init_processor import LessonInitProcessor

class LessonHandler:
    
    lesson_init_processor: LessonInitProcessor
    name = "lesson"
    
    class CallBackType(Enum):
        init_lesson = auto()
    
    def __init__(self, lesson_init_processor: LessonInitProcessor):
        self.lesson_init_processor = lesson_init_processor
        
    async def handle_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        cb_type: str
        ):
        query = update.callback_query
        await query.delete_message()
        if cb_type == self.CallBackType.init_lesson.value:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Начинаем урок"
            )
            await self.lesson_init_processor.init()