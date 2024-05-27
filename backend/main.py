import uuid
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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
    yield


app = FastAPI(lifespan=lifespan)


app.mount("/images", StaticFiles(directory="static/images"), name="images")


@app.get("/get_token/")
def get_token(tg_login: str):
    uuid_token = uuid.uuid5(uuid.NAMESPACE_DNS, tg_login)
    deps.redis.set_tg_login(tg_login=tg_login, uuid_token=str(uuid_token))
    return {"tg_login": tg_login, "uuid_token": str(uuid_token)}


@app.get("/authorization/")
def auth(uuid_token: str):
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    }
    if deps.redis.is_valid_token(uuid_token=uuid_token):
        return FileResponse("static/auth.html", headers=headers)
    return FileResponse("static/access_denied.html", headers=headers)


@app.post("/login/")
async def login(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    uuid_token: Annotated[str, Form()],
):
    if deps.validator.validation_for_login(login=login, password=password):
        tg_login = deps.redis.get_tg_login(uuid_token=uuid_token)
        deps.postgres.update_user_tg_login(tg_login=tg_login, login=login)
        return {"login": "success"}
    return {"login": "failed"}


@app.post("/register/")
async def register(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    words_in_lesson: Annotated[int, Form()],
    uuid_token: Annotated[str, Form()],
):
    if deps.validator.validation_for_registration(
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
        return {"registration": "success"}
    return {"registration": "failed"}


@app.get("/registration_complete/", response_class=HTMLResponse)
async def registration_complete():
    return FileResponse("static/registration_complete.html")


@app.get("/login_complete/", response_class=HTMLResponse)
async def login_complete():
    return FileResponse("static/login_complete.html")


@app.get("/logout/")
async def logout(uuid_token: str):
    tg_login = deps.redis.get_tg_login(uuid_token=uuid_token)
    deps.postgres.clear_tg_login(tg_login=tg_login)
    deps.redis.clear_data(data=tg_login)
    deps.redis.clear_data(data=uuid_token)
