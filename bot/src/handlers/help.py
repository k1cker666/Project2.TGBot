from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "В боте имеется 3 типа урока: обычный урок, повторение слов и практика.\n\n"
        + "В <b>обычном уроке</b> всегда даются новые слова, соответствующие вашему уровню.\n"
        + "В <b>повторении слов</b> даются слова, которые вы прошли в обычном уроке. "
        + "Чтобы слово имело статус 'выучено', необходимо повторить его 3 раза.\n"
        + "Ответы в этих двух типах уроков всегда учитываются в вашу статистику.\n"
        + "В <b>практике</b> даются слова любого уровня, независимо от того прошли вы их или нет.\n"
        + "Ответы в данном типе урока не учитываются в вашу статистику.\n\n"
        + "Соответственно, в <b>статистике</b> отображается информация о вашем текущем прогрессе.\n\n"
        + "В <b>настройках</b> вы можете поменять текущий уровень слов.\n\n"
        + "Если вы авторизованы и хотите сменить аккаунт, вы можете использовать команду <i>/logout</i>, "
        + "которая находится в вспомогательном меню.\n\n"
        + "Для дальнейших действий используйте команду <i>/start</i>"
    )
    await update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
