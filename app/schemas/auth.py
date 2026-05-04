from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

#Если логин реализован в стиле OAuth2 для Swagger,
#отдельная схема LoginRequest может быть не нужна,
# потому что логин принимается через OAuth2PasswordRequestForm,
# но схему токена всё равно нужно иметь, чтобы документировать ответ.