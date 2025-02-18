from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db import Base

class WebhookRequest(Base):
    __tablename__ = "webhook_requests"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    callback_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())  
