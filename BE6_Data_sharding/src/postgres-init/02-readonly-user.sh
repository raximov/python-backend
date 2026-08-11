#!/usr/bin/env bash
set -euo pipefail

if ! psql \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    -tAc "SELECT 1 FROM pg_roles WHERE rolname='shop_reader'" \
    | grep -q 1; then

    psql \
        --username "$POSTGRES_USER" \
        --dbname "$POSTGRES_DB" \
        -c "CREATE ROLE shop_reader LOGIN PASSWORD '${READONLY_DB_PASSWORD}';"
fi

psql \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" <<SQL
GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO shop_reader;
GRANT USAGE ON SCHEMA public TO shop_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO shop_reader;

ALTER DEFAULT PRIVILEGES FOR ROLE ${POSTGRES_USER}
IN SCHEMA public
GRANT SELECT ON TABLES TO shop_reader;

ALTER ROLE shop_reader SET default_transaction_read_only = on;
SQL
