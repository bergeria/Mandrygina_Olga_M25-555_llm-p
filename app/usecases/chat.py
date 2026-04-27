from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(
        self,
        chat_repository: ChatMessageRepository,
        openrouter_client: OpenRouterClient,
    ):
        self.chat_repository = chat_repository
        self.openrouter_client = openrouter_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
    ) -> str:
        history = await self.chat_repository.get_by_user_id(user_id)

        messages: list[dict[str, str]] = []

        if system:
            messages.append(
                {
                    "role": "system",
                    "content": system,
                }
            )

        for item in history:
            messages.append(
                {
                    "role": item.role,
                    "content": item.content,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        await self.chat_repository.create(
            user_id=user_id,
            role="user",
            content=prompt,
        )

        answer = await self.openrouter_client.ask(messages)

        await self.chat_repository.create(
            user_id=user_id,
            role="assistant",
            content=answer,
        )

        return answer
