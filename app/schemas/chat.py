from datetime import datetime

from pydantic import BaseModel

#В ChatRequest нужно предусмотреть поле prompt как основной текст запроса.
# Нужно предусмотреть поле system как необязательную системную инструкцию.
# Нужно предусмотреть max_history, чтобы управлять тем, сколько сообщений брать из истории.
# Нужно предусмотреть temperature, чтобы студент понимал, как управлять “креативностью” модели.

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
