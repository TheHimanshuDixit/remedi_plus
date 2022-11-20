from fastapi import APIRouter, Request
from decouple import config
import aiohttp

router = APIRouter()

__all__ = ("router",)


@router.get("/test")
async def test(request: Request):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(config("WHATSAPP_API")),
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "919996071403",
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}},
    }

    url = "https://graph.facebook.com/v15.0/103233349288425/messages"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as resp:
            print(resp.status)
            print(await resp.text())

    return {"message": "done"}
