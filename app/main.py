from fastapi import FastAPI
from app.routers.api import router as api_router
from mangum import Mangum

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message`": "Welcome to Stock Analysis!"}

handler = Mangum(app)