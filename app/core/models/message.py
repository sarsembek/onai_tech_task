from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_history_id = Column(Integer, ForeignKey("chat_history.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)

    chat_history = relationship("ChatHistory", back_populates="messages")