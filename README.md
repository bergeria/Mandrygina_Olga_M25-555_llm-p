№ В операционной системе должен быть установлен Python версии не ниже 3.11



\#Установка uv

pip install uv



&#x20;

\#Активировать виртуальное окружение

\# в MacOS/Linux

source .venv/bin/activate

\# в Windows

.venv\\Scripts\\activate.bat



&#x20;

\#Установить зависимости проекта

\#они прописаны в pyproject.toml

&#x20;

\# в Linux

uv pip install -r <(uv pip compile pyproject.toml)



\#В Windows / PowerShell

uv pip compile pyproject.toml -o requirements.txt

uv pip install -r requirements.txt



\#Далее необходимо зарегистрироваться на платформе OpenRouter и получить API-ключ,

\#который будет использоваться для взаимодействия с большой языковой моделью (LLM) через внешний сервис.

\#Полученный API-ключ необходимо вставить в файл .env в строку OPENROUTER\_API\_KEY=, после знака равенства, без кавычек.

\#Этот ключ будет использоваться серверным приложением для отправки запросов к OpenRouter.



\#Пример .env находится в файле .env.example

APP\_NAME=llm-p

ENV=local



JWT\_SECRET=change\_me\_super\_secret

JWT\_ALG=HS256

ACCESS\_TOKEN\_EXPIRE\_MINUTES=60



SQLITE\_PATH=./app.db



OPENROUTER\_API\_KEY=

OPENROUTER\_BASE\_URL=https://openrouter.ai/api/v1

OPENROUTER\_MODEL=nvidia/nemotron-3-super-120b-a12b:free

OPENROUTER\_SITE\_URL=https://example.com

OPENROUTER\_APP\_NAME=llm-fastapi-openrouter





\#Структура проекта

\#Архитектура с разделением ответственности: API → UseCases → Repositories → DB / Services

llm\_p/

├── pyproject.toml                 # Зависимости проекта (uv)

├── README.md                      # Описание проекта и запуск

├── .env.example                   # Пример переменных окружения

│

├── app/

│   ├── init.py

│   ├── main.py                    # Точка входа FastAPI

│   │

│   ├── core/                      # Общие компоненты и инфраструктура

│   │   ├── init.py

│   │   ├── config.py              # Конфигурация приложения (env → Settings)

│   │   ├── security.py            # JWT, хеширование паролей

│   │   └── errors.py              # Доменные исключения

│   │

│   ├── db/                        # Слой работы с БД

│   │   ├── init.py

│   │   ├── base.py                # DeclarativeBase

│   │   ├── session.py             # Async engine и sessionmaker

│   │   └── models.py              # ORM-модели (User, ChatMessage)

│   │

│   ├── schemas/                   # Pydantic-схемы (вход/выход API)

│   │   ├── init.py

│   │   ├── auth.py                # Регистрация, логин, токены

│   │   ├── user.py                # Публичная модель пользователя

│   │   └── chat.py                # Запросы и ответы LLM

│   │

│   ├── repositories/              # Репозитории (ТОЛЬКО SQL/ORM)

│   │   ├── init.py

│   │   ├── users.py               # Доступ к таблице users

│   │   └── chat\_messages.py       # Доступ к истории чатов

│   │

│   ├── services/                  # Внешние сервисы

│   │   ├── init.py

│   │   └── openrouter\_client.py   # Клиент OpenRouter / LLM

│   │

│   ├── usecases/                  # Бизнес-логика приложения

│   │   ├── init.py

│   │   ├── auth.py                # Регистрация, логин, профиль

│   │   └── chat.py                # Логика общения с LLM

│   │

│   └── api/                       # HTTP-слой (тонкие эндпоинты)

│       ├── init.py

│       ├── deps.py                # Dependency Injection

│       ├── routes\_auth.py         # /auth/\*

│       └── routes\_chat.py         # /chat/\*

│

└── app.db                         # SQLite база (создаётся при запуске)









\#запуск проекта

\#в каталоге проекта - выполнить



uv run uvicorn app.main:app --host 0.0.0.0 --port 8000



\# После запуска в любом браузере обратиться по адресу

\# если с локального компьютера

http://localhost:8000/docs

\# если другого компьютера

http://ip-address:8000/docs

\# ip-address - ip адрес компьютера на котором запущен проект, в firewall должны быть соответствующие правила.



\# После запуска необходимо пройти процедуру регистрации пользователя - логин и пароль

\# в качестве логина используйте email

\# Выберите пункт - POST/auth/register и нажмите кнопку 'Try it out'

\# в поле 'Request body' заполните логин и пароль, и потом нажмите 'Execute'



\# Далее во всех эндпоитах необходимо пользоваться механизмом 'Try it out' + 'Execute'

\# При необходимости заполняйте поле 'Request body'



\# Далее нужно выполнить вход в систему и получить JWT-токен,

\# который будет использоваться для доступа к защищённым эндпоинтам приложения.

\# Для этого в Swagger нажать Authorize и ввести данные - логин и пароль.

\# В нашем случае Swagger использует OAuth2PasswordRequestForm,

\# поэтому Swagger сам вызовет POST/auth/login, получит JWT и будет автоматически подставлять его.



\# Далее уже можно использовать чат и начать общаться с выбранной OPENROUTER\_MODEL



\# Примеры использования

\# скриншоты должны демонстрировать использование email формата student\_surname@email.com при регистрации.





\# Регистрация пользователя

!\[Register](screenshots/register.png)



\# Логин пользователя - логин и получение JWT

!\[Login](screenshots/login.png)



\# Авторизацию через Swagger

!\[Auth](screenshots/auth.png)



\# Chat пользователя - вызов POST /chat

!\[Chat](screenshots/chat.png)



\# Получение истории через GET /chat/history

!\[Get\_history](screenshots/get\_history.png)



\# Удаление истории через DELETE /chat/history

!\[Clear\_history](screenshots/clear\_history.png)

