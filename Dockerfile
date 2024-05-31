# Используем официальный образ Python версии 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копируем все файлы проекта в рабочую директорию
COPY . /app

# Копируем .env файл в рабочую директорию
COPY .env /app/.env

# Открываем порт, если необходимо
EXPOSE 8000

# Запускаем приложение
CMD ["python", "bot.py"]
