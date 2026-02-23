#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"
docker compose -f docker-compose.pgadmin.yml up -d

echo "pgAdmin available at http://localhost:5050"
echo "Login: admin@example.com / admin"
