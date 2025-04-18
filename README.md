# Telegram News Aggregator Bot

Бот-агрегатор новостей из Telegram-каналов об AI и технологиях. Позволяет просматривать посты из нескольких каналов в одной ленте, сохранять понравившиеся публикации и предлагать свои каналы для добавления.

## Функциональность

- Агрегация постов из заранее согласованного списка каналов (до 10 штук)
- Единая лента в хронологическом порядке
- Возможность лайкать и сохранять посты
- Просмотр и удаление сохраненных записей
- Форма для предложения своего канала

## Технический стек

- Python 3.11
- aiogram 3.x (async)
- Telethon для парсинга каналов
- SQLite 3 для хранения данных
- APScheduler для планирования задач
- Docker для контейнеризации

## Установка и запуск

### Предварительные требования

1. Python 3.11 или выше
2. Docker и Docker Compose (опционально)
3. Telegram API ключи (Bot Token, API ID, API Hash)

### Локальная установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/your-username/tg-news-feed.git
   cd tg-news-feed
   ```

2. Создайте виртуальное окружение и установите зависимости:
   ```
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` на основе `.env.example`:
   ```
   cp .env.example .env
   # Отредактируйте .env файл, добавив свои API-ключи
   ```

4. Запустите бота:
   ```
   python -m tg_news_feed.main
   ```

### Запуск через Docker

1. Создайте `.env` файл как указано выше

2. Соберите и запустите контейнер:
   ```
   docker-compose up -d
   ```

3. Просмотр логов:
   ```
   docker-compose logs -f
   ```

### Переменные окружения

| Переменная | Описание |
|------------|----------|
| BOT_TOKEN | Токен Telegram бота |
| API_ID | Telegram API ID |
| API_HASH | Telegram API Hash |
| ADMIN_IDS | ID администраторов (через запятую) |
| DB_PATH | Путь к файлу базы данных |
| FEEDBACK_FORM | URL формы для предложения каналов |
| PARSER_INTERVAL_MINUTES | Интервал обновления каналов в минутах |

## Команды бота

| Команда | Описание |
|---------|----------|
| /start | Начать работу с ботом |
| /feed | Показать ленту новостей |
| /saved | Показать сохраненные посты |
| /help | Показать справку |
| /suggest | Предложить свой канал |
| /stats | (только для админов) Показать статистику |
| /addchannel @username | (только для админов) Добавить канал |

## Структура проекта

```
tg_news_feed/
├─ bot/              # обработка команд Telegram
│   ├─ handlers/
│   │   ├─ user.py   # /start, /feed, кнопки
│   │   └─ admin.py  # скрытые админ-команды
│   └─ keyboards.py
├─ parser/           # фоновый сборщик постов
│   └─ fetcher.py
├─ storage/          # работа с БД
│   ├─ models.py
│   └─ repo.py
├─ scheduler.py      # планировщик
├─ config.py         # настройки
└─ main.py           # точка входа
```

## Миграция на PostgreSQL

Для миграции с SQLite на PostgreSQL:

1. Раскомментируйте разделы postgres и pgadmin в `docker-compose.yml`
2. Установите дополнительные зависимости:
   ```
   pip install psycopg2-binary
   ```
3. Измените строку подключения в `.env`:
   ```
   DB_PATH=postgresql://tgbot:password@postgres:5432/tg_news_feed
   ```
4. Запустите миграцию:
   ```
   alembic upgrade head
   ```

## Лицензия

MIT 