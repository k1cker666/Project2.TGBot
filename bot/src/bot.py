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
from loguru import logger
from src.dependencies import Dependencies
from src.models.callback import CallbackData

def start_bot(deps: Dependencies):
    
    def partial_deps(func):
        return partial(func, deps = deps)
        
    application = Application.builder().token(deps.config.bot_token).build()
    
    logger.info('Application was started')
    
    application.add_handler(CommandHandler("start", partial_deps(start)))
    application.add_handler(CommandHandler("help", help.help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo.echo))

    application.add_handler(CallbackQueryHandler(partial_deps(callback_handler)))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    deps: Dependencies
    ):
    await deps.start_handler.handle(update, context)

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    deps: Dependencies
    ):
    query = update.callback_query
    callback_data: CallbackData = CallbackData.from_string(query.data)
    if callback_data.cb_processor == deps.start_handler.name:
        await deps.start_handler.handle_callback(update, context, callback_data)
    if callback_data.cb_processor == deps.lesson_handler.name:
        await deps.lesson_handler.handle_callback(update, context, callback_data)
    if callback_data.cb_processor == deps.repetition_handler.name:
        await deps.repetition_handler.handle_callback(update, context, callback_data)