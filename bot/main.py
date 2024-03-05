from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from src.handlers import start, help, echo
from src import bot
from src.log import *


def main():
    application = Application.builder().token("7148494691:AAFgTWiU8919YwGHw6l8LTAAa3nxuhGUmO4").build()

    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("help", help.help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo.echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    bot.print_text()
    main()