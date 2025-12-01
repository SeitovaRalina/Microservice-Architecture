#!/bin/sh

echo "PostgreSQL is up. Running migrations..."
poetry run alembic upgrade head

echo "Starting FastAPI..."
exec poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload