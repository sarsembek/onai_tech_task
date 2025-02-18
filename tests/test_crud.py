from sqlalchemy.orm import Session
from app.core.crud.chat_history import get_chat_history, save_chat_message

def test_get_chat_history(db: Session):
    session_id = "test_session"
    messages = get_chat_history(db, session_id)
    assert messages == []

def test_save_chat_message(db: Session):
    session_id = "test_session"
    user_message = "Hello"
    bot_response = "Hi there!"
    save_chat_message(db, session_id, user_message, bot_response)
    messages = get_chat_history(db, session_id)
    assert messages == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]