#!/usr/bin/env bash

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found."
    echo "Create it first:"
    echo "  cp .env.example .env"
    exit 1
fi

echo "Starting PostgreSQL..."
docker compose up -d postgres

echo "Waiting for PostgreSQL..."
until docker exec shop_api_postgres \
    pg_isready -U shop_user -d shop_db >/dev/null 2>&1
do
    sleep 1
done

echo "Applying ShopAPI migrations..."
alembic upgrade head

echo "Applying Auth Service migrations..."
alembic -c auth_alembic.ini upgrade head

echo "Starting Authorization gRPC service on :50051..."
python -m auth_service.main &
AUTH_PID=$!

cleanup() {
    echo
    echo "Stopping Authorization Service..."
    kill "$AUTH_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

sleep 1

echo "Starting ShopAPI on :8000..."
uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 8000
