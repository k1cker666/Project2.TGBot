from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.handlers import start, help, echo

def start_bot(dependencies):
    application = Application.builder().token("7148494691:AAFgTWiU8919YwGHw6l8LTAAa3nxuhGUmO4").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help.help_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo.echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}, я бот повторяющий сообщения!")