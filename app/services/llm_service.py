import os
from openai import OpenAI
from sqlalchemy.orm import Session
from app.config import OPENAI_API_KEY
from app.core.crud.chat_history import get_chat_history, save_chat_message
import logging

client = OpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger(__name__)

def process_message(db: Session, session_id: str, message: str):
    """ Отправляет сообщение в GPT с учетом истории чата """

    try:
        history = get_chat_history(db, session_id)
        history.append({"role": "user", "content": message})

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history
        )

        bot_response = completion.choices[0].message.content

        save_chat_message(db, session_id, message, bot_response)
        logger.info(f"Message processed successfully for session ID: {session_id}")

        return bot_response
    except Exception as e:
        logger.error(f"Error processing message for session ID: {session_id}, Error: {e}")
        raise
