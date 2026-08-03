from fastapi import APIRouter

from app.api.v1.clients import router as clients_router
from app.api.v1.images import router as images_router
from app.api.v1.products import router as products_router
from app.api.v1.suppliers import router as suppliers_router

api_router = APIRouter()

api_router.include_router(
    clients_router,
    prefix="/clients",
)

api_router.include_router(
    suppliers_router,
    prefix="/suppliers",
)

api_router.include_router(
    products_router,
    prefix="/products",
)

api_router.include_router(images_router)