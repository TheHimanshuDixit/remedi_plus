from __future__ import annotations

from fastapi import FastAPI, Request

from tortoise.contrib.fastapi import register_tortoise
import constants
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .routes.reminders import router as reminders_router
from .routes.medicine import router as medicine_router
from .routes.test import router as test_router
from fastapi_utils.tasks import repeat_every
from models import Timer
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime

app = FastAPI()

app.include_router(reminders_router)
app.include_router(medicine_router)
app.include_router(test_router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
template = Jinja2Templates(directory="src/templates")


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@app.get("/about")
async def about(request: Request):
    print("new request")
    return template.TemplateResponse("About.html", {"request": request})


@app.get("/contact")
async def contact(request: Request):
    return template.TemplateResponse("Contactus.html", {"request": request})


@app.get("/search")
async def contact(request: Request):
    return template.TemplateResponse("Search.html", {"request": request})


@app.get("/addreminder")
async def add_reminder(request: Request):
    return template.TemplateResponse("Addreminder.html", {"request": request})


@app.get("/delreminder")
async def del_reminder(request: Request):
    return template.TemplateResponse("Delreminder.html", {"request": request})


@app.get("/myreminders")
async def my_reminders(request: Request):
    return template.TemplateResponse("Myreminders.html", {"request": request})


@app.on_event("startup")
@repeat_every(seconds=constants.SYNC_INTERVAL)
async def dispatch_reminders():
    records = await Timer.filter(
        expires__lte=datetime.now(constants.IST), dispatched=False
    )
    for record in records:
        await record.dispatch()


# @app.exception_handler(404)
# async def not_found(request: Request, exc):
#     return template.TemplateResponse("404.html", {"request": request})


register_tortoise(
    app,
    config=constants.TORTOISE_CONF,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
