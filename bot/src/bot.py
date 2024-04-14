from telegram import (
    Update
    )
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler
    )
from src.handlers import help, echo
from functools import partial
import json
from loguru import logger
from src.dependencies import Dependencies


def start_bot(deps: Dependencies):
    application = Application.builder().token(deps.config.bot_token).build()
    
    logger.info('Application was started')
    
    start_with_deps = partial(start, deps = deps)
    callback_handler_with_deps = partial(callback_handler, deps = deps)
    start_lesson_with_deps = partial(start_lesson, deps = deps)
    
    application.add_handler(CommandHandler("start", start_with_deps))
    application.add_handler(CommandHandler("help", help.help_command))

    application.add_handler(MessageHandler(filters.Text("Начать урок"), start_lesson_with_deps))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo.echo))

    application.add_handler(CallbackQueryHandler(callback_handler_with_deps))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    deps: Dependencies
    ):
    await deps.start_handler.handle(update, context)

async def start_lesson(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    deps: Dependencies
    ):
    await deps.lesson_handler.handle(update, context)

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    deps: Dependencies
    ):
    query = update.callback_query
    user_answer = json.loads(query.data)
    if user_answer["cb_processor"] == deps.start_handler.name:
        await deps.start_handler.handle_callback(update, context, user_answer["cb_type"])
    if user_answer["cb_processor"] == deps.lesson_handler.name:
        await deps.lesson_handler.handle(update, context)