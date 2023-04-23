from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from .endpoints import stocks

router = APIRouter()
router.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
