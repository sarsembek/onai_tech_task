from pydantic import BaseModel, ConfigDict
from typing import List

class MessageSchema(BaseModel):
    role: str
    content: str

    model_config = ConfigDict(from_attributes=True)

class ChatHistorySchema(BaseModel):
    session_id: str
    messages: List[MessageSchema]

    model_config = ConfigDict(from_attributes=True)
