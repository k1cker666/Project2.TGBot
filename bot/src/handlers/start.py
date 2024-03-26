from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}, я бот повторяющий сообщения!")
    await context.bot.send_message(
        chat_id = -1002085745418,
        text = f'Пользователь {user.mention_html()} начал чат с ботом',
        parse_mode = ParseMode.HTML
        )