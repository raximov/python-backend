#!/bin/sh
set -e

create_database() {
    db_name="$1"

    exists=$(
        psql -v ON_ERROR_STOP=1 \
            --username "$POSTGRES_USER" \
            --dbname postgres \
            -tAc "SELECT 1 FROM pg_database WHERE datname='${db_name}'"
    )

    if [ "$exists" != "1" ]; then
        echo "Creating database: ${db_name}"

        psql -v ON_ERROR_STOP=1 \
            --username "$POSTGRES_USER" \
            --dbname postgres \
            -c "CREATE DATABASE \"${db_name}\";"
    else
        echo "Database ${db_name} already exists"
    fi
}

create_database "photo_db_1"
create_database "photo_db_2"
create_database "photo_db_3"
create_database "photo_db_4"
