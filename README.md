# Claw-Agent

Мультиплатформенный AI-агент с поддержкой Telegram и MAX ботов.

## Возможности

- 🌅 Утренние сообщения (08:00 + погода)
- 🌙 Вечерние сообщения (23:00 + план)
- 🔔 Напоминания (T-10, T-0)
- 🎲 Jitter (случайные интервалы)
- 👥 Несколько аккаунтов

## Установка

```bash
# Клонировать репозиторий
git clone <repo-url>
cd claw-agent

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить окружение
cp .env.example .env
# Отредактировать .env с токенами
```

## Конфигурация (.env)

```env
# Telegram бот
TELEGRAM_BOT_TOKEN=your_telegram_token

# MAX бот  
MAX_BOT_TOKEN=your_max_token

# Админ (чат ID через запятую)
ADMIN_CHAT_IDS=123456789

# Яндекс Погода
YANDEX_WEATHER_API_KEY=your_yandex_key

# Расписание
MORNING_HOUR=8
MORNING_MINUTE=0
NIGHT_HOUR=23
NIGHT_MINUTE=0

# Jitter (минуты)
JITTER_MIN=15
JITTER_MAX=30

# Город
DEFAULT_CITY=Казань

# Часовой пояс
TIMEZONE=Europe/Moscow
```

## Запуск

```bash
# Локально
python main.py

# Docker
docker-compose up -d
```

## Docker сборка

```bash
docker build -t claw-agent .
docker run -d --env-file .env claw-agent
```

## Команды бота

- `/start` - Запуск
- `/help` - Помощь
- `/status` - Статус
- `/settings` - Настройки
- `/schedule` - Расписание