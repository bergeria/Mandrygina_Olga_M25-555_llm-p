from app.core.errors import LLMServiceError
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
        #Берем историю сообщений пользователя
        history = await self.chat_repository.get_by_user_id(user_id)

        #Начинаем собирать список сообщений для модели
        messages: list[dict[str, str]] = []

        #Если есть system-инструкция, то добавляем system-сообщение
        if system:
            messages.append(
                {
                    "role": "system",
                    "content": system,
                }
            )

        #Добавляем историю сообщений пользователя в список сообщений для модели
        for item in history:
            messages.append(
                {
                    "role": item.role,
                    "content": item.content,
                }
            )

        #Добавляем текущий prompt как сообщение пользователя
        #в список сообщений для модели
        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        #Сохраняем prompt в БД как сообщение пользователя
        await self.chat_repository.create(
            user_id=user_id,
            role="user",
            content=prompt,
        )

        #Делаем запрос к OpenRouter
        answer = await self.openrouter_client.ask(messages)

        #Проверяем ответ на None
        if not answer:
            raise LLMServiceError("OpenRouter вернул пустой ответ")

        #Ответ сохраняем в БД как сообщение роли assistant
        #и возвращаем текст ответа
        await self.chat_repository.create(
            user_id=user_id,
            role="assistant",
            content=answer,
        )

        return answer
