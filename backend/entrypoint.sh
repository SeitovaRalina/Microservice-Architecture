#!/bin/sh

echo "PostgreSQL is up. Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload