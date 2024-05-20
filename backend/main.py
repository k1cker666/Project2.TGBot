import uuid
from contextlib import asynccontextmanager
from functools import partial
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from redis.exceptions import ConnectionError
from src.dependencies import Dependencies, DependenciesBuilder
from src.log import logger_config, logger_main
from src.validator import validation_for_registration
from starlette.responses import FileResponse


deps: Dependencies


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_config
    logger_main
    global deps
    deps = DependenciesBuilder.build()
    global validation_for_registration_with_psql
    validation_for_registration_with_psql = partial(
        validation_for_registration, postgres=deps.postgres
    )
    yield


app = FastAPI(lifespan=lifespan)


app.mount(
    "/images", StaticFiles(directory="backend/static/images"), name="images"
)


@app.get("/check_pg/")
def check_pg_connection():
    if deps.postgres.check_connect():
        return {"pg_connection": True}
    return {"pg_connection": False}


@app.get("/check_redis/")
def check_redis_connection():
    try:
        deps.redis.connection.ping()
        return {"redis_connection": True}
    except ConnectionError:
        return {"redis_connection": False}


@app.get("/get_token/")
def get_token(tg_login: str):
    uuid_token = uuid.uuid5(uuid.NAMESPACE_DNS, tg_login)
    deps.redis.set_tg_login(tg_login=tg_login, uuid_token=str(uuid_token))
    return {"tg_login": tg_login, "uuid_token": str(uuid_token)}


@app.get("/authorization/")
def auth(uuid_token: str):
    if deps.redis.is_valid_token(uuid_token=uuid_token):
        return FileResponse("backend/static/auth.html")
    return FileResponse("backend/static/access_denied.html")


@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    uuid_token: Annotated[str, Form()],
):
    if username != "1" or password != "1":
        raise HTTPException(
            status_code=401,
            detail="Неверное имя пользователя или пароль",
        )
    # TODO: Сделать проверку юзера
    return {"message": "login succes"}


@app.post("/register/")
async def register(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    words_in_lesson: Annotated[int, Form()],
    uuid_token: Annotated[str, Form()],
):
    if validation_for_registration_with_psql(
        login=login,
        password=password,
        confirm_password=confirm_password,
    ):
        tg_login = deps.redis.get_tg_login(uuid_token=uuid_token)
        deps.postgres.add_user_in_database(
            tg_login=tg_login,
            login=login,
            password=password,
            words_in_lesson=words_in_lesson,
        )
        return {}


@app.get("/registration_complete/", response_class=HTMLResponse)
async def registration_complete():
    return FileResponse("backend/static/registration_complete.html")


@app.get("/login_complete/", response_class=HTMLResponse)
async def login_complete():
    return FileResponse("backend/static/login_complete.html")
