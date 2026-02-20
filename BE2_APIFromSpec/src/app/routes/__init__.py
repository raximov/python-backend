from flask import Flask
from flask_restx import Api

from app.routes.client_routes import client_ns
from app.routes.product_routes import product_ns
from app.routes.supplier_routes import supplier_ns
from app.routes.image_routes import image_ns


def register_api(app: Flask) -> None:
    """Register all API namespaces with Flask-RESTX."""
    api = Api(
        app,
        version="1.0",
        title="Store API",
        description="REST API for an Appliance Store. "
                    "Manage clients, products, suppliers, and images.",
        doc="/swagger/index.html",
        prefix="/api/v1",
    )

    api.add_namespace(client_ns, path="/clients")
    api.add_namespace(product_ns, path="/products")
    api.add_namespace(supplier_ns, path="/suppliers")
    api.add_namespace(image_ns, path="/images")
