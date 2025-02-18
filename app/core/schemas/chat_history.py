from pydantic import BaseModel
from typing import List

class MessageSchema(BaseModel):
    role: str
    content: str

    class Config:
        orm_mode = True

class ChatHistorySchema(BaseModel):
    session_id: str
    messages: List[MessageSchema]

    class Config:
        orm_mode = True
