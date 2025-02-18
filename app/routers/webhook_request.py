from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.schemas.webhook_request import WebhookRequestSchema
from app.core.models.webhook_request import WebhookRequest
from app.db import get_db
from app.services.webhook_processor import process_webhook_request
import httpx
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from rq import Queue
from redis import Redis
import os

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_conn = Redis.from_url(redis_url)
task_queue = Queue(connection=redis_conn)

@router.post("/webhook")
@limiter.limit("10/minute")
async def handle_webhook(request: Request, request_data: WebhookRequestSchema, db: Session = Depends(get_db)):
    # Сохранение запроса в БД
    webhook_entry = WebhookRequest(message=request_data.message, callback_url=str(request_data.callback_url))
    db.add(webhook_entry)
    db.commit()
    db.refresh(webhook_entry)

    try:
        # Enqueue the task to Redis Queue
        job = task_queue.enqueue(process_webhook_request, request_data.dict(), webhook_entry.id)
        logger.info(f"Webhook processed successfully for ID: {webhook_entry.id}")
        return {"status": "accepted", "id": webhook_entry.id, "job_id": job.id}
    except httpx.HTTPError as e:
        logger.error(f"Failed to send callback for ID: {webhook_entry.id}, Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send callback: {e}")
    except Exception as e:
        logger.error(f"An error occurred for ID: {webhook_entry.id}, Error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
