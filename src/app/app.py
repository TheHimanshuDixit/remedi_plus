from __future__ import annotations

from fastapi import FastAPI, Request

from tortoise.contrib.fastapi import register_tortoise
import constants
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

template = Jinja2Templates(directory="src/templates")


@app.get("/")
async def root(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@app.exception_handler(404)
async def not_found(request: Request, exc):
    return template.TemplateResponse("404.html", {"request": request})


register_tortoise(
    app,
    config=constants.TORTOISE_CONF,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
