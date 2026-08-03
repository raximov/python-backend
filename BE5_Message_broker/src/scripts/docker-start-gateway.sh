#!/bin/sh
set -eu

echo "ShopAPI migratsiyalari bajarilmoqda..."
alembic upgrade head

echo "FastAPI Gateway ishga tushirilmoqda..."
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000
