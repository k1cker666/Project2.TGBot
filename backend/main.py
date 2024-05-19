import uuid
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from redis.exceptions import ConnectionError
from src.dependencies import Dependencies, DependenciesBuilder
from src.log import logger_config, logger_main
from starlette.responses import FileResponse


deps: Dependencies


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_config
    logger_main
    global deps
    deps = DependenciesBuilder.build()
    deps.postgres.is_login_available("admin")
    deps.postgres.is_login_available("1212")
    yield


app = FastAPI(lifespan=lifespan)


app.mount(
    "/images", StaticFiles(directory="backend/static/images"), name="iamges"
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
    deps.redis.set_token(tg_login=tg_login, uuid_token=str(uuid_token))
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
    word_count: Annotated[int, Form()],
    uuid_token: Annotated[str, Form()],
):
    if len(login) < 5:
        raise HTTPException(
            status_code=409,
            detail="Логин должен состоять как минимум из 5 символов",
        )
    if not deps.postgres.is_login_available(login):
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
    # TODO: Здесь нужно добавить регистрацию пользователя в базе данных
    return {"message": "reg succces"}


@app.get("/registration_complete/", response_class=HTMLResponse)
async def registration_complete():
    return FileResponse("backend/static/registration_complete.html")


@app.get("/login_complete/", response_class=HTMLResponse)
async def login_complete():
    return FileResponse("backend/static/login_complete.html")
