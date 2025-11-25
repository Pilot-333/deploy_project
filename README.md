# alpina_digital

Django-приложение для создания и управления ботами на основе GPT API.

## Функциональность

- **CRUD операции для ботов** - создание, чтение, обновление, удаление ботов
- **CRUD операции для сценариев** - управление диалоговыми сценариями
- **CRUD операции для шагов сценариев** - настройка отдельных шагов взаимодействия
- **Интеграция с GPT API** - использование возможностей OpenAI для генерации ответов
- **Управление сценариями** - хранение и редактирование через административный интерфейс
- **История выполнений** - отслеживание диалогов пользователей с ботами

## Технологии

- **Backend**: Django 4.2, Django REST Framework
- **База данных**: SQLite (для разработки), поддерживает PostgreSQL, MySQL
- **AI**: OpenAI GPT API
- **Аутентификация**: Session-based, Basic Auth
- **Документация API**: Django REST Framework Browsable API

## Установка и настройка

### Предварительные требования

- Python 3.8+
- Git
- OpenAI API ключ

### 1. Клонирование репозитория

git clone <repository-url>

### 2. Создание и активация виртуального окружения
python -m venv .venv
.venv\Scripts\activate

### 3. Установка зависимостей
pip install -r requirements.txt


### 4. Настройка переменных окружения

# Создайте файл .env на основе примера
.env

# Отредактируйте .env файл
notepad .env  # Windows

**Содержимое .env файла:**
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your-actual-openai-api-key-here
REDIS_URL=redis://localhost:6379/0

### 5. Настройка базы данных

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

### 6. Создание суперпользователя

python manage.py createsuperuser

### 7. Создание тестовых данных (опционально)

python manage.py create_test_data

### 8. Запуск сервера

python manage.py runserver

Приложение будет доступно по адресу: http://127.0.0.1:8000/

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

## Тестирование

### Запуск тестов

python manage.py test

### Тестирование API

# Используйте встроенный тестовый скрипт
python test_api.py

# Или используйте curl команды
curl -X GET http://127.0.0.1:8000/api/bots/