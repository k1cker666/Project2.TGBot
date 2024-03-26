from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help!")
    user = update.effective_user