from fastapi import APIRouter, Request

router = APIRouter()

__all__ = ("router",)


@router.get("/test")
async def test(request: Request):
    ...
