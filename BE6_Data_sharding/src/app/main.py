from pathlib import Path
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.auth import router as auth_router
from app.api.v1.router import api_router
from app.core.exceptions import BadRequestError, NotFoundError
from app.cache.redis_client import close_redis_client
from app.messaging.consumer import ProductUpdateConsumer
from app.middleware.authorization import AuthorizationMiddleware
from app.api.realtime import router as realtime_router
from app.realtime.broadcaster import broadcast_product_update


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    ),
)

product_update_consumer = ProductUpdateConsumer(
    on_product_updated=broadcast_product_update,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await product_update_consumer.start()

    try:
        yield
    finally:
        await product_update_consumer.stop()
        close_redis_client()


app = FastAPI(
    title="ShopAPI",
    description="REST API for a household appliances store",
    version="1.0.0",
    docs_url="/swagger/index.html",
    redoc_url=None,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(AuthorizationMiddleware)

CLIENTS_DIR = Path(__file__).resolve().parent.parent / "clients"

app.mount(
    "/clients",
    StaticFiles(
        directory=str(CLIENTS_DIR),
        html=True,
    ),
    name="clients",
)


@app.exception_handler(NotFoundError)
async def not_found_handler(
    request: Request,
    exc: NotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


@app.exception_handler(BadRequestError)
async def bad_request_handler(
    request: Request,
    exc: BadRequestError,
):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
            }
        ),
    )


@app.get(
    "/",
    tags=["Health"],
    summary="API health check",
)
def health_check():
    return {
        "status": "ok",
        "service": "ShopAPI",
    }


app.include_router(auth_router)
app.include_router(realtime_router)

app.include_router(
    api_router,
    prefix="/api/v1",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault(
        "securitySchemes",
        {},
    )

    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    public_paths = {
        "/",
        "/register",
        "/auth",
        "/reset",
        "/sse/products",
    }

    http_methods = {
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "options",
        "head",
    }

    for path_name, path_data in openapi_schema.get(
        "paths",
        {},
    ).items():
        for method, operation in path_data.items():
            if method.lower() not in http_methods:
                continue

            if not isinstance(operation, dict):
                continue

            responses = operation.get("responses", {})

            if "422" in responses:
                validation_response = responses.pop("422")
                validation_response["description"] = "Bad Request"
                responses.setdefault("400", validation_response)

            if path_name in public_paths:
                operation["security"] = []
            else:
                operation["security"] = [
                    {"BearerAuth": []}
                ]

                responses.setdefault(
                    "401",
                    {
                        "description": "Unauthorized",
                    },
                )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
