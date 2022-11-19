from fastapi import APIRouter, Request
from models import Timer
from datetime import datetime, timedelta
from constants import IST
import dateparser


__all__ = ("router",)
router = APIRouter(prefix="/reminder")


@router.get("/")
async def rem_main(request: Request):
    ...


@router.get("/create/fake")
async def fake_reminders(request: Request):
    await Timer.create(
        name="paracetamol",
        dosage="1 tablet",
        phone=1234567890,
        expires=datetime.now(IST) + timedelta(minutes=1),
    )
    await Timer.create(
        name="paracetamol",
        dosage="1 tablet",
        phone=1234567890,
        expires=datetime.now(IST) + timedelta(minutes=2),
    )
    await Timer.create(
        name="something",
        dosage="1 tablet",
        phone=1234567890,
        expires=datetime.now(IST) + timedelta(minutes=3),
    )
    await Timer.create(
        name="something",
        dosage="100 ml",
        phone=1234567890,
        expires=datetime.now(IST) + timedelta(minutes=4),
    )

    return {"message": "done"}


@router.get("/create")
async def rem_create(request: Request, time: str):
    ...
    parsed = dateparser.parse(
        time,
        settings={
            "RELATIVE_BASE": datetime.now(tz=IST),
            "TIMEZONE": "Asia/Kolkata",
            "RETURN_AS_TIMEZONE_AWARE": True,
        },
    )

    if not parsed:
        return {"message": "Invalid time"}

    while not parsed > datetime.now(IST):
        parsed += timedelta(days=1)

    return {"parsed_time": parsed.strftime("%d %b %Y %H:%M:%S %Z")}


@router.get("/mine")
async def rem_mine(request: Request, phone: int):
    records = await Timer.filter(phone=phone).order_by("expires").all()
    return [dict(record) for record in records]


@router.get("/delete")
async def rem_delete(request: Request, id: int):
    await Timer.filter(pk=id).delete()
    return {"status": "ok"}
