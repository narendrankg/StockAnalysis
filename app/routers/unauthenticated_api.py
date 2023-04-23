from fastapi import APIRouter

from .endpoints import authentication

router = APIRouter()
router.include_router(authentication.router, prefix="/token", tags=["token"])