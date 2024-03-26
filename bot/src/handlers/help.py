from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help!")
    user = update.effective_user
    await context.bot.send_message(
        chat_id = -1002085745418,
        text = f'Пользователь {user.mention_html()} просит помощи',
        parse_mode = ParseMode.HTML
        )