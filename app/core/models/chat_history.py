from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

    messages = relationship("Message", back_populates="chat_history", cascade="all, delete-orphan")
