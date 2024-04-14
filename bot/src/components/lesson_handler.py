from telegram import (
    Update
)
from telegram.ext import ContextTypes
from src.components.lesson_init_processor import LessonInitProcessor

class LessonHandler:
    
    lesson_init_processor: LessonInitProcessor
    name = "lesson"
    
    def __init__(self, lesson_init_processor: LessonInitProcessor):
        self.lesson_init_processor = lesson_init_processor
        
    async def handle(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        ):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Начинаем урок"
        )