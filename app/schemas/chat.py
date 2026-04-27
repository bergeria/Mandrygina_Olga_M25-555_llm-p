from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    system: str | None = None


class ChatResponse(BaseModel):
    answer: str


class ChatMessageCreate(BaseModel):
    message: str


class ChatMessageRead(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
