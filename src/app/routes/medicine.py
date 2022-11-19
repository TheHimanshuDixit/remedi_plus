from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import aiohttp

__all__ = ("router",)

router = APIRouter()


@router.get("medicine/details")
async def get_med_details(request: Request, name: str):
    ...
