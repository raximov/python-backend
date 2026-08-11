# BE6 — Data Sharding and Google OAuth

School 21 backend project with PostgreSQL photo sharding and Google OAuth 2.0.

## Features

- FastAPI Shop API / Gateway
- gRPC Authorization Service
- Existing email/password authentication
- Google OAuth 2.0 authentication
- Local Google users without stored passwords
- Separate Photo Service
- HTTP communication between Shop API and Photo Service
- Four PostgreSQL photo shards
- UUID-based shard routing
- Redis image caching
- RabbitMQ events
- WebSocket and SSE
- Docker Compose
- Alembic migrations
- Pytest

## Photo Sharding

Photos are routed using the first hexadecimal character of the UUID:

- `0-3` → `photo_db_1`
- `4-7` → `photo_db_2`
- `8-b` → `photo_db_3`
- `c-f` → `photo_db_4`

All four databases run on the same PostgreSQL server.

## Architecture

```text
Client
  |
  v
Shop API / Gateway :8000
  |
  +---- gRPC ----> Auth Service :50051
  |
  +---- HTTP ----> Photo Service :8001
                         |
                         v
                    UUID Router
                  /    /    \    \
                DB1   DB2   DB3   DB4




Google OAuth Flow

/auth/google/login
        |
        v
      Google
        |
        v
/auth/google/callback
        |
        v
Google UserInfo
        |
        v
gRPC GoogleLogin
        |
        v
Local User + JWT                



Run:

docker compose up -d

docker compose up -d gateway auth-service

Browser:  http://127.0.0.1:8000/auth/google/login