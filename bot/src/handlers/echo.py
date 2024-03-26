from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)
    user = update.effective_user
    await context.bot.send_message(
        chat_id = -1002085745418,
        text = f'{user.mention_html()}: {update.message.text}',
        parse_mode = ParseMode.HTML
        )