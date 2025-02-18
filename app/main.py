from fastapi import FastAPI
from app.routers import webhook_request
from app.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address
from redis import Redis
from rq import Queue

app = FastAPI()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Redis Queue
redis_conn = Redis.from_url("redis://redis:6379/0")
task_queue = Queue(connection=redis_conn)

app.include_router(webhook_request.router)

@app.get("/info")
def get_app_info():
    return {
        "app_name": settings.app_name,
        "openai_api_key": f"{settings.openai_api_key[:4]}****"
    }
