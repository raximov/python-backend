# Nginx Task Solution (Chapter II)

This folder contains a complete Nginx setup for the Store API project:

- Reverse proxy for Store API backends.
- Routing:
  - `/api` -> `/api/v1`
  - `/api/v1` -> Swagger UI
  - `/` -> static distribution (`index.html` + `image.png`)
  - `/admin` -> pgAdmin
  - `/status` -> Nginx status page
- Balancing for GET/HEAD requests on `/api/v1` and `/api/v2` across 3 backends in `2:1:1` ratio.
- Non-GET requests go to the main backend only.
- Proxy caching for GET/HEAD requests except `/api*`.
- Gzip compression enabled for text-based content types only.
- HTTPS configured with a local self-signed certificate.

## Paths

- Nginx config: `src/nginx.conf`, `src/conf.d/store.conf`
- Static files: `src/static/index.html`, `src/static/image.png`
- Scripts: `src/scripts/*`
- Optional pgAdmin stack: `src/docker-compose.pgadmin.yml`

## Prerequisites

- Store API source (BE2):
  - `/home/user01/Desktop/be/BE2_APIFromSpec.ID_1269320-1/src`
- Installed tools:
  - `nginx`, `openssl`
  - `docker` + `docker compose` (only for pgAdmin)

## 1) Start 3 backend instances

```bash
cd /home/user01/Desktop/BE/BE3_Nginx_Pro.ID_1269323-1
./src/scripts/start_backends.sh
```

This starts:
- Main backend: `:5000`
- Read-only replica #1: `:5001`
- Read-only replica #2: `:5002`

To stop them:

```bash
./src/scripts/stop_backends.sh
```

## 2) Start pgAdmin for `/admin`

```bash
./src/scripts/start_pgadmin.sh
```

pgAdmin login:
- Email: `admin@example.com`
- Password: `admin`

To stop:

```bash
./src/scripts/stop_pgadmin.sh
```

## 3) Generate local certificate

```bash
./src/scripts/generate_cert.sh store-api.local
```

Add hosts record if needed:

```text
127.0.0.1 store-api.local
```

## 4) Start Nginx with this config

```bash
./src/scripts/start_nginx.sh
```

Stop Nginx:

```bash
./src/scripts/stop_nginx.sh
```

## Endpoints

- HTTP:
  - `http://localhost:8081/`
  - `http://localhost:8081/api`
  - `http://localhost:8081/api/v1/swagger/index.html`
  - `http://localhost:8081/api/v2/swagger/index.html`
  - `http://localhost:8081/admin/`
  - `http://localhost:8081/status`
- HTTPS:
  - `https://store-api.local:8444/`
  - `https://store-api.local:8444/api/v1/swagger/index.html`

## Notes

- This setup uses high ports (`8081`, `8444`) to run without root privileges.
- To use `80`/`443`, update `listen` directives in `src/conf.d/store.conf` and run Nginx with privileges.
