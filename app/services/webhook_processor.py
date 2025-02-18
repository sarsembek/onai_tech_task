from sqlalchemy.orm import Session
from app.db import get_db
from app.core.schemas.webhook_request import WebhookRequestSchema
from app.services.llm_service import process_message
import httpx
import logging

logger = logging.getLogger(__name__)

def process_webhook_request(request_data: WebhookRequestSchema, db: Session):
    """Обрабатывает входящее сообщение, отправляет его в LLM и возвращает ответ на callback URL"""
    
    session_id = str(request_data.callback_url)

    try:
        response_message = process_message(db, session_id, request_data.message)
    except Exception as e:
        logger.error(f"Error processing message for session ID: {session_id}, Error: {e}")
        raise

    with httpx.Client() as client:
        try:
            client.post(str(request_data.callback_url), json={"response": response_message})
            logger.info(f"Callback sent successfully for session ID: {session_id}")
        except httpx.HTTPError as e:
            logger.error(f"Failed to send callback for session ID: {session_id}, Error: {e}")
            raise

    return response_message
