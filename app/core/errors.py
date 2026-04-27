class AppError(Exception):
    """Базовая ошибка приложения."""


class UserAlreadyExistsError(AppError):
    """Пользователь с таким email уже существует."""


class InvalidCredentialsError(AppError):
    """Неверный email или пароль."""


class UserNotFoundError(AppError):
    """Пользователь не найден."""


class LLMServiceError(AppError):
    """Ошибка при обращении к LLM-сервису."""
