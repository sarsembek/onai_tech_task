from sqlalchemy.orm import Session
from app.core.models.chat_history import ChatHistory
from app.core.models.webhook_request import WebhookRequest
from app.core.models.message import Message

def test_create_chat_history(db: Session):
    chat_history = ChatHistory(session_id="test_session")
    message = Message(role="user", content="Hello", chat_history=chat_history)
    chat_history.messages.append(message)
    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)
    assert chat_history.id is not None
    assert chat_history.session_id == "test_session"
    assert len(chat_history.messages) == 1
    assert chat_history.messages[0].role == "user"
    assert chat_history.messages[0].content == "Hello"

def test_create_webhook_request(db: Session):
    webhook_request = WebhookRequest(message="Test message", callback_url="http://example.com")
    db.add(webhook_request)
    db.commit()
    db.refresh(webhook_request)
    assert webhook_request.id is not None
    assert webhook_request.message == "Test message"
    assert webhook_request.callback_url == "http://example.com"