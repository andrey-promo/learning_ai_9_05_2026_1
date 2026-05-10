# Telegram LLM Bot

Telegram-бот, который отвечает на текстовые сообщения через языковую модель (OpenRouter API).

## Требования

- macOS
- [uv](https://docs.astral.sh/uv/) — менеджер зависимостей Python
- Docker (опционально, для запуска в контейнере)

## Быстрый старт

### 1. Настройка окружения

Скопируйте файл с переменными окружения и заполните значения:

```bash
cp .env.example .env
```

Обязательные переменные в `.env`:

| Переменная | Описание |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен бота из [@BotFather](https://t.me/BotFather) |
| `OPENROUTER_API_KEY` | Ключ API с [openrouter.ai](https://openrouter.ai) |
| `OPENROUTER_MODEL` | Модель, например `openai/gpt-oss-20b:free` |
| `SYSTEM_PROMPT` | Системный промпт (роль ассистента) |

### 2. Запуск без Docker

```bash
make install   # установить зависимости
make run       # запустить бота
```

### 3. Запуск в Docker

```bash
make docker-build   # собрать образ
make docker-run     # запустить контейнер
```

## Деплой в Railway

1. Зарегистрируйтесь на [railway.app](https://railway.app) и создайте новый проект.
2. Подключите репозиторий: **New Project → Deploy from GitHub repo**.
3. В Railway Dashboard → **Variables** добавьте обязательные переменные окружения:

| Переменная | Описание |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен бота из [@BotFather](https://t.me/BotFather) |
| `OPENROUTER_API_KEY` | Ключ API с [openrouter.ai](https://openrouter.ai) |
| `OPENROUTER_MODEL` | Модель, например `openai/gpt-oss-20b:free` |
| `SYSTEM_PROMPT` | Системный промпт (роль ассистента) |

4. Railway автоматически обнаружит `railway.toml` и `Dockerfile`, соберёт образ и запустит бота.
5. При каждом `git push` Railway пересобирает образ и перезапускает сервис.
6. Логи доступны в Railway Dashboard → вкладка **Logs**.

> Открытый порт не нужен — бот работает на long polling без HTTP-сервера.

## Команды бота

- `/start` — приветствие
- `/help` — краткая справка
- Любой текст — ответ от языковой модели

## Заметки

- История диалога хранится в памяти процесса и сбрасывается при перезапуске.
- Не запускайте несколько экземпляров бота одновременно — Telegram не поддерживает параллельный long polling.
