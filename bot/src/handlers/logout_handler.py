import requests
from src.repository.user_repository import UserRepository
from telegram import Update
from telegram.ext import ContextTypes


class LogoutHandler:

    backend_url: str
    user_repository: UserRepository

    def __init__(self, backend_url: str, user_repository: UserRepository):
        self.backend_url = backend_url
        self.user_repository = user_repository

    def __get_token(self, tg_login: str) -> str:
        r = requests.get(
            url=f"{self.backend_url}/get_token/", params={"tg_login": tg_login}
        )
        return r.json()["uuid_token"]

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.user_repository.fetch_user_by_tg_login(
            tg_login=update.effective_user.username
        ):
            uuid_token = self.__get_token(
                tg_login=update.effective_user.username
            )
            requests.get(
                url=f"{self.backend_url}/logout/",
                params={"uuid_token": uuid_token},
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Вы успешно вышли из системы",
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Вы не авторизованы в системе",
            )
