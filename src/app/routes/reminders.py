from fastapi import APIRouter, Request

__all__ = ("router",)
router = APIRouter(prefix="/reminder")


@router.get("/")
async def rem_main(request: Request):
    ...


@router.get("/create")
async def rem_create(request: Request):
    ...


@router.get("/mine")
async def rem_mine(request: Request):
    ...


@router.get("/delete")
async def rem_delete(request: Request):
    ...
