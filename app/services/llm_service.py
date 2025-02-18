import os
from openai import OpenAI
from sqlalchemy.orm import Session
from app.config import OPENAI_API_KEY
from app.core.crud.chat_history import get_chat_history, save_chat_message, create_chat_history
from app.core.crud.message import create_message
from app.core.schemas.chat_history import MessageSchema, ChatHistorySchema
import logging

client = OpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger(__name__)

def process_message(db: Session, session_id: str, message: str):
    """ Sends a message to GPT with chat history """

    try:
        # Get chat history for the session
        chat_history = get_chat_history(db, session_id)
        
        if chat_history is None:
            # Create a new chat history if it doesn't exist
            chat_history = create_chat_history(db, ChatHistorySchema(session_id=session_id, messages=[]))
            logger.info(f"Created new chat history for session ID: {session_id}")
        
        # Create a Message instance instead of appending a dict
        new_message = create_message(db, MessageSchema(role="user", content=message), chat_history.id)
        
        # Append the message to the history (in case it's not automatically done)
        chat_history.messages.append(new_message)
        
        # Send the history to GPT for completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": msg.role, "content": msg.content} for msg in chat_history.messages]
        )

        # Get the bot's response from GPT
        bot_response = completion.choices[0].message.content

        # Save the bot's response to the database
        save_chat_message(db, session_id, message, bot_response)

        logger.info(f"Message processed successfully for session ID: {session_id}")

        return bot_response

    except Exception as e:
        logger.error(f"Error processing message for session ID: {session_id}, Error: {e}")
        raise

