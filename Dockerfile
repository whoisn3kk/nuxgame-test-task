FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install uv
COPY pyproject.toml uv.lock ./

WORKDIR /app

RUN uv sync --locked

COPY ./backend .

EXPOSE 8000

CMD sh -c "uv run python manage.py migrate && uv run gunicorn game_api.wsgi:application --bind 0.0.0.0:8000"