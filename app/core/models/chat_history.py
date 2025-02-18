from sqlalchemy import Column, Integer, String, JSON, DateTime, func, MetaData
from app.db import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    messages = Column(JSON, nullable=False, default=[])  
    created_at = Column(DateTime, default=func.now()) 
