from pydantic import BaseModel
from typing import List, Dict, Any

class ChatHistorySchema(BaseModel):
    session_id: str
    messages: List[Dict[str, Any]]
