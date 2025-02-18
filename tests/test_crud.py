from sqlalchemy.orm import Session
from app.core.crud.chat_history import get_chat_history, save_chat_message
from app.core.models.chat_history import ChatHistory

def test_get_chat_history(db: Session):
    session_id = "test_session"
    chat_history = get_chat_history(db, session_id)
    assert chat_history is None

def test_save_chat_message(db: Session):
    session_id = "test_session"
    user_message = "Hello"
    bot_response = "Hi there!"
    save_chat_message(db, session_id, user_message, bot_response)
    chat_history = get_chat_history(db, session_id)
    assert chat_history is not None
    assert len(chat_history.messages) == 1
    assert chat_history.messages[0].role == "assistant"
    assert chat_history.messages[0].content == "Hi there!"
