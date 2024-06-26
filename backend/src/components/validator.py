from fastapi import HTTPException
from src.components.psql_core import PostgreSQL


class Validator:

    postgres: PostgreSQL

    def __init__(self, postgres: PostgreSQL):
        self.postgres = postgres

    def validation_for_registration(
        self, login: str, password: str, confirm_password: str
    ) -> bool:
        if len(login) < 5:
            raise HTTPException(
                status_code=409,
                detail="Логин должен состоять как минимум из 5 символов",
            )
        if not self.postgres.is_login_available(login):
            raise HTTPException(
                status_code=409,
                detail="Такой логин уже используется",
            )
        if password != confirm_password:
            raise HTTPException(
                status_code=400,
                detail="Пароли не совпадают",
            )
        if len(password) < 8:
            raise HTTPException(
                status_code=409,
                detail="Пароль должен состоять как минимум из 8 символов",
            )
        return True

    def validation_for_login(self, login: str, password: str):
        user = self.postgres.fetch_user_by_login(login=login)
        if user is None or password != user["password"]:
            raise HTTPException(
                status_code=409,
                detail="Неверное имя пользователя или пароль",
            )
        return True
