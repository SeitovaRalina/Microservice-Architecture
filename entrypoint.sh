#!/bin/sh

echo "Waiting for PostgreSQL to start..."
while ! python -c "
import socket
import sys
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('db', 5432))
    sock.close()
    sys.exit(result)
except Exception as e:
    sys.exit(1)
"; do
  sleep 0.5
done

echo "PostgreSQL is up. Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload