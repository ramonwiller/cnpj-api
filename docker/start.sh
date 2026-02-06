#!/usr/bin/env bash
set -e

echo "Starting application..."
echo "Environment: ${ENV:-development}"

# Decide como iniciar baseado no ambiente
if [ "$ENV" = "production" ]; then
  echo "Running with Gunicorn (production)"
  exec gunicorn app.main:app \
    -k uvicorn.workers.UvicornWorker \
    --workers ${WORKERS:-4} \
    --bind 0.0.0.0:8000

else
  echo "Running with Uvicorn (dev/staging)"
  exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000
fi