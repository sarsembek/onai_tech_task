from sqlalchemy.orm import Session
from app.core.models.message import Message
from app.core.schemas.chat_history import MessageSchema
from typing import List, Optional

def get_message_by_id(db: Session, message_id: int) -> Optional[Message]:
    """ Получает сообщение по ID """
    return db.query(Message).filter(Message.id == message_id).first()

def get_messages_by_chat_history_id(db: Session, chat_history_id: int) -> List[Message]:
    """ Получает все сообщения по chat_history_id """
    return db.query(Message).filter(Message.chat_history_id == chat_history_id).all()

def create_message(db: Session, message: MessageSchema, chat_history_id: int) -> Message:
    """ Создает новое сообщение """
    db_message = Message(
        chat_history_id=chat_history_id,
        role=message.role,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_message(db: Session, message_id: int, message: MessageSchema) -> Optional[Message]:
    """ Обновляет существующее сообщение """
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db_message.role = message.role
        db_message.content = message.content
        db.commit()
        db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int) -> Optional[Message]:
    """ Удаляет сообщение по ID """
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message