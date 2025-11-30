# alpina_digital

Django-приложение для создания и управления ботами на основе GPT API.

## Особенности

- **CRUD операции** для ботов, сценариев и шагов взаимодействия
- **Интеллектуальные ответы** на основе ключевых слов (вместо OpenAI используется заглушка)
- **Автоматический деплой** через GitHub Actions на VPS
- **Docker контейнеризация** для простого развертывания
- **CI/CD пайплайн** для автоматических обновлений при каждом изменении кода
- **Готовая инфраструктура** с Nginx и контейнеризацией

## Технологии

- **Backend**: Django 4.2, Django REST Framework
- **База данных**: SQLite (для учебного проекта)
- **AI**: Интеллектуальная заглушка с контекстными ответами
- **Контейнеризация**: Docker, Docker Compose
- **Web сервер**: Nginx
- **CI/CD**: GitHub Actions
- **Хостинг**: GitHub Container Registry + VPS (Timeweb Cloud)
- **Аутентификация**: Session-based, Basic Auth

## Установка и настройка

### Предварительные требования

- Python 3.8+
- Git
- OpenAI API ключ

# Клонирование репозитория
git clone https://github.com/Pilot-333/deploy_project.git
cd alpina_digital

# Создание и активация виртуального окружения
python -m venv .venv
.venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
# Создайте файл .env на основе примера
.env.example

# Отредактируйте .env файл
notepad .env  # Windows

**Содержимое .env файла:**
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your-actual-openai-api-key-here

# Применение миграций БД
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
Приложение будет доступно по адресу: http://127.0.0.1:8000/

# Деплой на VPS
Приложение автоматически развертывается на VPS при каждом пуше в ветку `main` через GitHub Actions.

**Текущий сервер**: http://5.23.55.202

## API Endpoints

### Основные endpoints

| Метод | Endpoint | Описание |
|-------|----------|-----------|
| `GET` | `/` | Главная страница |
| `GET` | `/api/root/` | Информация о API |
| `GET` | `/admin/` | Административная панель |

### Боты (Bots)

| Метод | Endpoint | Описание |
|-------|----------|-----------|
| `GET` | `/api/bots/` | Список всех ботов |
| `POST` | `/api/bots/` | Создание нового бота |
| `GET` | `/api/bots/{id}/` | Детальная информация о боте |
| `PUT` | `/api/bots/{id}/` | Обновление бота |
| `DELETE` | `/api/bots/{id}/` | Удаление бота |
| `POST` | `/api/bots/{id}/chat/` | Чат с ботом |

### Сценарии (Scenarios)

| Метод | Endpoint | Описание |
|-------|----------|-----------|
| `GET` | `/api/scenarios/` | Список сценариев |
| `POST` | `/api/scenarios/` | Создание сценария |
| `GET` | `/api/scenarios/{id}/` | Детали сценария |
| `PUT` | `/api/scenarios/{id}/` | Обновление сценария |
| `DELETE` | `/api/scenarios/{id}/` | Удаление сценария |
| `GET` | `/api/scenarios/{id}/steps/` | Шаги сценария |

### Шаги (Steps)

| Метод | Endpoint | Описание |
|-------|----------|-----------|
| `GET` | `/api/steps/` | Список шагов |
| `POST` | `/api/steps/` | Создание шага |
| `GET` | `/api/steps/{id}/` | Детали шага |
| `PUT` | `/api/steps/{id}/` | Обновление шага |
| `DELETE` | `/api/steps/{id}/` | Удаление шага |

### Выполнения (Executions)

| Метод | Endpoint | Описание |
|-------|----------|-----------|
| `GET` | `/api/executions/` | История выполнений |
| `POST` | `/api/executions/` | Создание записи выполнения |
| `GET` | `/api/executions/{id}/` | Детали выполнения |
| `PUT` | `/api/executions/{id}/` | Обновление выполнения |
| `DELETE` | `/api/executions/{id}/` | Удаление выполнения |

## Примеры использования API

### Создание бота
curl -X POST http://127.0.0.1:8000/api/bots/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Бот-консультант",
    "description": "Бот для консультаций",
    "bot_type": "chat",
    "gpt_model": "gpt-3.5-turbo",
    "creativity_level": 0.7,
    "max_tokens": 1000,
    "system_prompt": "Ты полезный ассистент для консультаций.",
    "is_active": True,
    "created_by": 1
  }'

### Чат с ботом
curl -X POST http://127.0.0.1:8000/api/bots/1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Привет! Расскажи о возможностях системы",
    "user_session": "user_123"
  }'

### Создание сценария
curl -X POST http://127.0.0.1:8000/api/scenarios/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Сценарий приветствия",
    "description": "Базовый сценарий знакомства с пользователем",
    "bot": 1,
    "is_active": true
  }'

## Модели данных

### Bot
- `name` - Имя бота
- `description` - Описание
- `bot_type` - Тип бота (completion/chat)
- `gpt_model` - Модель GPT
- `creativity_level` - Уровень креативности
- `max_tokens` - Максимальное количество токенов
- `system_prompt` - Системный промпт
- `is_active` - Активен ли бот
- `created_by` - Автор

### Scenario
- `name` - Название сценария
- `description` - Описание
- `bot` - Бот
- `initial_step` - Начальный шаг
- `is_active` - Активен ли сценарий

### Step
- `name` - Название шага
- `step_type` - Тип шага (message/question/condition/api_call)
- `scenario` - Связанный сценарий
- `content` - Содержание шага (JSON)
- `order` - Порядок в сценарии
- `next_step` - Следующий шаг

### BotExecution
- `bot` - Бот
- `scenario` - Сценарий
- `user_session` - Сессия пользователя
- `current_step` - Текущий шаг
- `conversation_history` - История разговора
- `is_completed` - Завершено ли выполнение

## Административный интерфейс
Доступен по адресу: http://127.0.0.1:8000/admin/

Возможности:
- Управление ботами, сценариями, шагами
- Просмотр истории выполнений
- Настройка параметров GPT
- Управление пользователями

## Docker развертывание

### Локальный запуск с Docker
# Клонирование
git clone https://github.com/Pilot-333/deploy_project.git
cd alpina_digital

# Настройка окружения
cp .env.example .env
# Отредактируйте .env

# Запуск
docker-compose up -d

### Продакшен деплой

Приложение автоматически развертывается через GitHub Actions при каждом обновлении кода.

## CI/CD Пайплайн

GitHub Actions автоматически выполняет:
1. ** Сборка Docker образа** - использует Dockerfile
2. ** Публикация в GitHub Container Registry** - ghcr.io/larasedova/alpina_gpt_builder:latest
3. ** Подключение к VPS по SSH** - использует настроенные секреты
4. ** Копирование конфигурационных файлов** - docker-compose.yml, nginx.conf
5. ** Остановка старых контейнеров** - graceful shutdown
6. ** Запуск новых контейнеров** - с обновленным образом
7. ** Выполнение миграций БД** - автоматическое обновление схемы
8. ** Сбор статических файлов** - collectstatic

## Структура проекта

 alpina_digital/
├── .github/
│   └── workflows/
│       └── deploy.yml                  # CI/CD пайплайн
├── bots/                               # Основное приложение
│   ├── migrations/                     # Миграции БД
│   ├── management/
│   │   └── commands/
│   │       └── create_test_data.py     # Создание тестовых данных
│   ├── templates/                      # HTML шаблоны
│   ├── __init__.py
│   ├── admin.py                        # Админ-панель
│   ├── apps.py                         # Конфигурация приложения
│   ├── models.py                       # Модели данных
│   ├── serializers.py                  # Сериализаторы DRF
│   ├── services.py                     # Логика AI-ответов (заглушка)
│   ├── urls.py                         # URL приложения
│   └── views.py                        # Представления API
├── alpina_digital/                     # Настройки проекта
│   ├── __init__.py
│   ├── asgi.py                         # ASGI конфигурация
│   ├── settings.py                     # Настройки Django
│   ├── urls.py                         # Корневые URL
│   └── wsgi.py                         # WSGI конфигурация
├── db
│   └── .gitkeep
├── nginx/
│   └── nginx.conf                      # Конфигурация Nginx
├── .dockerignore                       # Игнор для Docker
├── .env.example                        # Шаблон переменных окружения
├── .gitignore                          # Git ignore
├── docker-compose.yml                  # Docker Compose
├── Dockerfile                          # Docker образ
├── manage.py                           # Django manage скрипт
├── README.md                           # Документация
└── requirements.txt                    # Зависимости Python

## Настройка для продакшена
### Переменные окружения

Создайте файл `.env` на основе `.env.example`:

SECRET_KEY=your-very-secret-key
DEBUG=False
ALLOWED_HOSTS=5.23.55.202,localhost,127.0.0.1
OPENAI_API_KEY=demo-mode-no-key-required

### Настройки GitHub Secrets
Для работы CI/CD необходимо настроить секреты в репозитории:
- `CR_PAT` - Personal Access Token GitHub
- `SECRET_KEY` - Секретный ключ Django
- `VPS_HOST` - `5.23.55.202`
- `VPS_USER` - `root`
- `VPS_SSH_KEY` - Приватный SSH ключ

## Тестирование
# Запуск тестов
python manage.py test

# Создание тестовых данных
python manage.py create_test_data

# Тестирование API
curl -X GET http://5.23.55.202/api/bots/

## Особенности реализации

### AI-заглушка
Вместо реального OpenAI API используется интеллектуальная заглушка, которая:
- Анализирует ключевые слова в запросах
- Генерирует контекстно-релевантные ответы
- Имитирует задержку реального API
- Поддерживает различные типы ботов (поддержка, обучение, продажи)

### Автоматический деплой
Система автоматически развертывает приложение при каждом изменении кода:
- Образ собирается на GitHub Actions
- Публикуется в GitHub Container Registry
- Развертывается на VPS через SSH
- Выполняются миграции и сбор статики

*Приложение доступно по адресу: http://5.23.55.202*