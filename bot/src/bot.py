from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
    )
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
    )
from src.handlers import help, echo
from functools import partial
# from dependencies import Dependencies

def start_bot(dependencies):
    application = Application.builder().token("7148494691:AAFgTWiU8919YwGHw6l8LTAAa3nxuhGUmO4").build()
    
    start_mes = partial(start, dependencies = dependencies)
    
    application.add_handler(CommandHandler("start", start_mes))
    application.add_handler(CommandHandler("help", help.help_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo.echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, dependencies):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}, я бот, которы поможет тебе выучить иностранные слова!")
    buttons = KeyboardButton('Авторизация')
    but_reply = ReplyKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Выбери действие",
        reply_markup=but_reply
    )