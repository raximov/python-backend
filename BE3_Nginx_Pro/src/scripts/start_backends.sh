#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

API_SRC="${API_SRC:-/home/user01/Desktop/be/BE2_APIFromSpec.ID_1269320-1/src}"
API_VENV="${API_VENV:-${API_SRC}/.venv}"
PYTHON_BIN="${PYTHON_BIN:-${API_VENV}/bin/python}"

RUNTIME_DIR="${PROJECT_ROOT}/runtime"
LOG_DIR="${PROJECT_ROOT}/logs"

mkdir -p "${RUNTIME_DIR}" "${LOG_DIR}"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Python interpreter not found: ${PYTHON_BIN}" >&2
  exit 1
fi

DB_PATH="${DB_PATH:-${API_SRC}/store.db}"
if [[ ! -f "${DB_PATH}" ]]; then
  echo "Database file not found: ${DB_PATH}" >&2
  exit 1
fi

MAIN_DB_URL="${DATABASE_URL_MAIN:-sqlite:///${DB_PATH}}"
RO_DB_URL="${DATABASE_URL_REPLICA:-sqlite:///file:${DB_PATH}?mode=ro&uri=true}"

start_instance() {
  local name="$1"
  local port="$2"
  local db_url="$3"

  local pid_file="${RUNTIME_DIR}/${name}.pid"
  local log_file="${LOG_DIR}/${name}.log"

  if [[ -f "${pid_file}" ]] && kill -0 "$(cat "${pid_file}")" 2>/dev/null; then
    echo "${name} already running with PID $(cat "${pid_file}")"
    return
  fi

  if ss -ltn "( sport = :${port} )" | grep -q ":${port}"; then
    echo "Port ${port} is already in use. Skipping ${name}."
    return
  fi

  nohup env \
    PORT="${port}" \
    FLASK_ENV=production \
    DATABASE_URL="${db_url}" \
    "${PYTHON_BIN}" "${SCRIPT_DIR}/run_instance.py" \
    --api-src "${API_SRC}" \
    --port "${port}" \
    --config production \
    >"${log_file}" 2>&1 &

  local pid=$!
  echo "${pid}" >"${pid_file}"
  sleep 1

  if kill -0 "${pid}" 2>/dev/null; then
    echo "Started ${name} on :${port} (PID ${pid})"
  else
    echo "Failed to start ${name}. Check ${log_file}" >&2
    rm -f "${pid_file}"
    exit 1
  fi
}

start_instance "backend-main" 5000 "${MAIN_DB_URL}"
start_instance "backend-ro1" 5001 "${RO_DB_URL}"
start_instance "backend-ro2" 5002 "${RO_DB_URL}"

echo "Backend startup complete."
