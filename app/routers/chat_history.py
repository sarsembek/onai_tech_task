from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.schemas.chat_history import ChatHistorySchema
from app.core.models.chat_history import ChatHistory
from app.core.crud.chat_history import (
    get_all_chat_histories,
    get_chat_history_by_id,
    create_chat_history,
    update_chat_history,
    delete_chat_history
)
from app.db import get_db

router = APIRouter()

@router.get("/chat_histories", response_model=List[ChatHistorySchema])
def read_chat_histories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chat_histories = get_all_chat_histories(db)
    return chat_histories

@router.get("/chat_histories/{chat_history_id}", response_model=ChatHistorySchema)
def read_chat_history(chat_history_id: int, db: Session = Depends(get_db)):
    chat_history = get_chat_history_by_id(db, chat_history_id)
    if chat_history is None:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return chat_history

@router.post("/chat_histories", response_model=ChatHistorySchema)
def create_new_chat_history(chat_history: ChatHistorySchema, db: Session = Depends(get_db)):
    return create_chat_history(db, chat_history)

@router.put("/chat_histories/{chat_history_id}", response_model=ChatHistorySchema)
def update_existing_chat_history(chat_history_id: int, chat_history: ChatHistorySchema, db: Session = Depends(get_db)):
    updated_chat_history = update_chat_history(db, chat_history_id, chat_history)
    if updated_chat_history is None:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return updated_chat_history

@router.delete("/chat_histories/{chat_history_id}", response_model=ChatHistorySchema)
def delete_existing_chat_history(chat_history_id: int, db: Session = Depends(get_db)):
    deleted_chat_history = delete_chat_history(db, chat_history_id)
    if deleted_chat_history is None:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return deleted_chat_history