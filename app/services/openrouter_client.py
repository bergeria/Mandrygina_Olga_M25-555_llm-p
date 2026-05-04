import httpx

from app.core.config import settings
from app.core.errors import LLMServiceError

class OpenRouterClient:
    async def ask(self, messages: list[dict[str, str]]) -> str:
        """

        :rtype: str
        """
        url = f"{settings.openrouter_base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }

        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=60,
            )

        if response.status_code >= 400:
            raise LLMServiceError(response.text)

        data = response.json()

        #OpenRouter/модели иногда возвращает content в разных форматах.
        #Но пока не будем заниматься нормализацией ответов.

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMServiceError("Invalid OpenRouter response") from exc

        #Чудные ответы иногда приходят...
        answer = content

        if not answer:
            raise LLMServiceError("Empty OpenRouter response")

        return answer

