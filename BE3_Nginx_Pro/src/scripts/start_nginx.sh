#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CERT_FILE="${PROJECT_ROOT}/certs/store-api.local.crt"
KEY_FILE="${PROJECT_ROOT}/certs/store-api.local.key"

if [[ ! -f "${CERT_FILE}" || ! -f "${KEY_FILE}" ]]; then
  echo "Certificate files missing. Generating default certificate for store-api.local"
  "${SCRIPT_DIR}/generate_cert.sh" store-api.local
fi

mkdir -p "${PROJECT_ROOT}/logs" "${PROJECT_ROOT}/cache" "${PROJECT_ROOT}/tmp"

nginx -p "${PROJECT_ROOT}" -c nginx.conf

echo "Nginx started with prefix ${PROJECT_ROOT}"
echo "HTTP:  http://localhost:8081/"
echo "HTTPS: https://store-api.local:8444/"
