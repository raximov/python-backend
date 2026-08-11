#!/bin/sh
set -eu

echo "Auth migratsiyalari bajarilmoqda..."
alembic -c auth_alembic.ini upgrade head

echo "gRPC Auth Service ishga tushirilmoqda..."
exec python -m auth_service.main
