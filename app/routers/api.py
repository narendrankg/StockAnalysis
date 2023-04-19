from fastapi import APIRouter

from .endpoints import stocks
from .endpoints import token

router = APIRouter()
router.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
router.include_router(token.router, prefix="/token", tags=["token"])