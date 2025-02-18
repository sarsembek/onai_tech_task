from sqlalchemy.orm import Session
from app.core.models.chat_history import ChatHistory
from app.core.crud.message import create_message
from app.core.models.message import Message
from app.core.schemas.chat_history import ChatHistorySchema, MessageSchema
from typing import List, Optional

def get_chat_history(db: Session, session_id: str) -> Optional[ChatHistory]:
    """ Получает историю чата по session_id """
    return db.query(ChatHistory).filter(ChatHistory.session_id == session_id).first()

def save_chat_message(db: Session, session_id: str, user_message: str, bot_response: str):
    """ Сохраняет сообщение пользователя и ответ бота """
    chat = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).first()

    if chat:
        # Append the new messages
        create_message(db, MessageSchema(role="user", content=user_message), chat.id)
        create_message(db, MessageSchema(role="assistant", content=bot_response), chat.id)
    else:
        # If no chat entry exists, create a new one with the first two messages
        chat = ChatHistory(session_id=session_id)
        db.add(chat)
        db.commit()  # Commit to get the chat ID
        db.refresh(chat)  # Refresh to make sure it's in the session
        create_message(db, MessageSchema(role="user", content=user_message), chat.id)
        create_message(db, MessageSchema(role="assistant", content=bot_response), chat.id)

    # Commit the changes to the database
    db.commit()

def get_all_chat_histories(db: Session) -> List[ChatHistory]:
    """ Получает все истории чатов """
    return db.query(ChatHistory).all()

def get_chat_history_by_id(db: Session, chat_history_id: int) -> Optional[ChatHistory]:
    """ Получает историю чата по ID """
    return db.query(ChatHistory).filter(ChatHistory.id == chat_history_id).first()

def create_chat_history(db: Session, chat_history: ChatHistorySchema) -> ChatHistory:
    """ Создает новую историю чата """
    db_chat_history = ChatHistory(
        session_id=chat_history.session_id,
        messages=[Message(**message.dict()) for message in chat_history.messages]
    )
    db.add(db_chat_history)
    db.commit()
    db.refresh(db_chat_history)
    return db_chat_history

def update_chat_history(db: Session, chat_history_id: int, chat_history: ChatHistorySchema) -> Optional[ChatHistory]:
    """ Обновляет существующую историю чата """
    db_chat_history = db.query(ChatHistory).filter(ChatHistory.id == chat_history_id).first()
    if db_chat_history:
        db_chat_history.session_id = chat_history.session_id
        db_chat_history.messages = [Message(**message.dict()) for message in chat_history.messages]
        db.commit()
        db.refresh(db_chat_history)
    return db_chat_history

def delete_chat_history(db: Session, chat_history_id: int) -> Optional[ChatHistory]:
    """ Удаляет историю чата по ID """
    db_chat_history = db.query(ChatHistory).filter(ChatHistory.id == chat_history_id).first()
    if db_chat_history:
        db.delete(db_chat_history)
        db.commit()
    return db_chat_history
