from contextlib import asynccontextmanager

from fastapi import FastAPI

from photo_service.api.routes.photos import router as photos_router
from photo_service.db.init_db import init_shard_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_shard_tables()
    yield


app = FastAPI(
    title="BE6 Photo Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(photos_router)


@app.get("/healthz", tags=["Health"])
def healthcheck():
    return {
        "status": "ok",
        "service": "photo-service",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "photo_service.main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
    )
