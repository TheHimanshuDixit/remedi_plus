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


def parse_time(time: str):
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

    return parsed


@router.post("/create")
async def rem_create(request: Request):
    form = await request.form()

    _range = int(form.get("time_slot"))
    for i in range(0, _range):
        await Timer.create(
            name=form.get("medname"),
            dosage=form.get("Dosage") + " " + form.get("dosetype"),
            phone=form.get("mobno"),
            expires=parse_time(form.get("time_slot{0}".format(i))),
        )

    return {"message": "Created {} timers for you.".format(_range)}


@router.get("/mine")
async def rem_mine(request: Request, phone: int):
    records = await Timer.filter(phone=phone).order_by("expires").all()
    _list = [dict(record) for record in records]
    for _ in _list:
        _["expires"] = _["expires"].strftime("%d %b %Y %H:%M")
        _["created_at"] = _["created_at"].strftime("%d %b %Y %H:%M")

    return _list


@router.post("/delete")
async def rem_delete(request: Request):
    form = await request.form()
    await Timer.filter(id__in=form.keys()).delete()
    return {"message": "Deleted {} timers for you.".format(len(form.keys()))}
