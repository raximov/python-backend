#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ -f "${PROJECT_ROOT}/logs/nginx.pid" ]]; then
  nginx -p "${PROJECT_ROOT}" -c nginx.conf -s stop
  echo "Nginx stopped."
else
  echo "Nginx PID file not found; nothing to stop."
fi
