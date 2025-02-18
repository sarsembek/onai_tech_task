from sqlalchemy.orm import Session
from app.core.models.chat_history import ChatHistory
import json

def get_chat_history(db: Session, session_id: str):
    """ Получает историю чата по session_id """
    chat = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).first()
    return chat.messages if chat else []

def save_chat_message(db: Session, session_id: str, user_message: str, bot_response: str):
    """ Сохраняет сообщение пользователя и ответ бота """
    chat = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).first()

    if chat:
        history = chat.messages
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_response})
        chat.messages = history
    else:
        chat = ChatHistory(session_id=session_id, messages=[
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": bot_response}
        ])
        db.add(chat)

    db.commit()
