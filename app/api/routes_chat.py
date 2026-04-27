from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_repository, get_chat_usecase, get_current_user_id
from app.core.errors import LLMServiceError
from app.repositories.chat_messages import ChatMessageRepository
from app.schemas.chat import ChatMessageRead, ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=data.prompt,
            system=data.system,
        )
    except LLMServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="LLM service error",
        ) from exc

    return ChatResponse(answer=answer)


@router.get("/history", response_model=list[ChatMessageRead])
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_repository: ChatMessageRepository = Depends(get_chat_repository),
):
    return await chat_repository.get_by_user_id(user_id)


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_repository: ChatMessageRepository = Depends(get_chat_repository),
):
    await chat_repository.delete_by_user_id(user_id)
