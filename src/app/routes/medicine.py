from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import aiohttp
from decouple import config

__all__ = ("router",)

router = APIRouter(prefix="/medicine")


@router.get("/details")
async def get_med_details(request: Request, name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(config("MED_API") + name) as response:
            data = await response.json()
            return data
