# Claw-Agent - Agent Instructions

## Проект
Мультиплатформенный AI-агент с поддержкой Telegram и MAX ботов.

## Команды запуска
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
python main.py

# Docker
docker-compose up -d --build
```

## Тестирование
```bash
# Запуск с отладкой
python -m debugpy main.py

# Проверка импортов
python -c "from main import main; print('OK')"
```

## Структура
- `bot/` - Telegram и MAX боты
- `core/` - Конфигурация, планировщик
- `db/` - SQLite модели и репозиторий
- `jobs/` - Задачи (morning, night, reminders)
- `services/` - Погода, сообщения
- `main.py` - Точка входа
- `.env.example` - Шаблон конфигурации