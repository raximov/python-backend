#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -f ".env" ]]; then
    set -a
    source .env
    set +a
fi

: "${DATABASE_URL:?DATABASE_URL is required}"
: "${READONLY_DATABASE_URL:?READONLY_DATABASE_URL is required}"

nohup env DATABASE_URL="$DATABASE_URL" \
uvicorn app.main:app --host 127.0.0.1 --port 8000 \
> /tmp/be3-backend-8000.log 2>&1 &

nohup env DATABASE_URL="$READONLY_DATABASE_URL" \
uvicorn app.main:app --host 127.0.0.1 --port 8001 \
> /tmp/be3-backend-8001.log 2>&1 &

nohup env DATABASE_URL="$READONLY_DATABASE_URL" \
uvicorn app.main:app --host 127.0.0.1 --port 8002 \
> /tmp/be3-backend-8002.log 2>&1 &

echo "Backends started:"
echo "  MAIN      -> 127.0.0.1:8000"
echo "  READ ONLY -> 127.0.0.1:8001"
echo "  READ ONLY -> 127.0.0.1:8002"
