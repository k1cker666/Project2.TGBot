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


def start_bot(deps):
    application = Application.builder().token("7148494691:AAFgTWiU8919YwGHw6l8LTAAa3nxuhGUmO4").build()
    
    start_mes = partial(deps.start_handler.start, deps = deps)
    callback = partial(callback_handler, deps = deps)
    
    application.add_handler(CommandHandler("start", start_mes))
    
    application.add_handler(CallbackQueryHandler(callback))
    
    application.add_handler(CommandHandler("help", help.help_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo.echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, deps):
    query = update.callback_query
    user_answer = json.loads(query.data.replace("'",'"'))
    if user_answer["cb_processor"] == deps.start_handler.name:
        await deps.start_handler.handle_callback(update, context, user_answer["cb_type"])