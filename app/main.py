from fastapi import FastAPI
from routers.authenticated_api import router as authenticated_api_router
from routers.unauthenticated_api import router as unauthenticated_api_router
from mangum import Mangum
from slowapi.util import get_remote_address
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(authenticated_api_router, prefix="/api/v1")
app.include_router(unauthenticated_api_router)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
async def root():
    return {"message`": "Welcome to Stock Analysis!"}

handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)