# BE5 — Message Broker

School 21 backend project.

Ushbu loyiha RabbitMQ orqali mahsulot narxi va ombordagi sonini avtomatik
yangilash, WebSocket va SSE orqali klientlarga real vaqtda xabar yuborish
hamda mahsulot rasmlarini Redis’da keshlashni namoyish qiladi.

## Architecture

```text
Event Generator Worker
        |
        | product.attributes.updated
        v
     RabbitMQ
        |
        v
FastAPI Gateway Consumer
        |
        +----> PostgreSQL product update
        |
        +----> WebSocket clients
        |
        +----> SSE clients

FastAPI Gateway ----gRPC----> Authorization Service
FastAPI Gateway ------------> Redis image cache
