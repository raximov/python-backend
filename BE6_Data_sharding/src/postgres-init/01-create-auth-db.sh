#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname postgres <<-EOSQL
    SELECT 'CREATE DATABASE auth_db OWNER $POSTGRES_USER'
    WHERE NOT EXISTS (
        SELECT FROM pg_database WHERE datname = 'auth_db'
    )\gexec
EOSQL
