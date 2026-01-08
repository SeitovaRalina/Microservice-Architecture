FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.2.1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get remove -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN useradd -m appuser && \
    chown appuser:appuser /app

COPY --chown=appuser:appuser pyproject.toml poetry.lock ./

USER appuser

RUN poetry install --no-root --no-ansi --no-interaction --only main

COPY --chown=appuser:appuser . .

CMD ["sh", "-c", "sleep 15 && poetry run celery -A src.core.celery_app.celery_app worker --loglevel=info -c 4 -Q publish"]