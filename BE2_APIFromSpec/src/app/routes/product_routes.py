from flask import request
from flask_restx import Namespace, Resource, fields

from app.dto.product_dto import ProductCreateDTO, ProductDecreaseStockDTO
from app.mappers.product_mapper import ProductMapper
from app.repositories.product_repository import ProductRepository

product_ns = Namespace("Products", description="Product management operations")

# ---- Swagger Models ----
product_input_model = product_ns.model("ProductInput", {
    "name": fields.String(required=True, description="Product name",
                          example="Washing Machine X200"),
    "category": fields.String(required=True, description="Product category",
                              example="Washing Machines"),
    "price": fields.Float(required=True, description="Product price", example=29999.99),
    "available_stock": fields.Integer(description="Available stock quantity",
                                      example=50, default=0),
    "supplier_id": fields.String(description="Supplier UUID",
                                 example="550e8400-e29b-41d4-a716-446655440000"),
})

product_response_model = product_ns.model("ProductResponse", {
    "id": fields.String(readonly=True, description="Product UUID",
                        example="550e8400-e29b-41d4-a716-446655440000"),
    "name": fields.String(description="Product name", example="Washing Machine X200"),
    "category": fields.String(description="Product category", example="Washing Machines"),
    "price": fields.Float(description="Product price", example=29999.99),
    "available_stock": fields.Integer(description="Available stock quantity", example=50),
    "last_update_date": fields.DateTime(description="Last update timestamp"),
    "supplier_id": fields.String(description="Supplier UUID"),
    "image_id": fields.String(description="Image UUID"),
})

decrease_stock_model = product_ns.model("DecreaseStock", {
    "quantity": fields.Integer(required=True, description="Quantity to decrease",
                               example=5, min=1),
})

error_model = product_ns.model("ProductError", {
    "message": fields.String(description="Error message"),
})


@product_ns.route("")
class ProductList(Resource):
    """Product collection resource."""

    @product_ns.doc("get_available_products")
    @product_ns.marshal_list_with(product_response_model)
    @product_ns.response(200, "Success")
    def get(self):
        """Get all available products (stock > 0)."""
        products = ProductRepository.get_all_available()
        return [ProductMapper.to_dto(p) for p in products], 200

    @product_ns.doc("create_product")
    @product_ns.expect(product_input_model, validate=False)
    @product_ns.marshal_with(product_response_model, code=201)
    @product_ns.response(400, "Validation error", error_model)
    @product_ns.response(201, "Product created")
    def post(self):
        """Add a new product."""
        if not request.is_json:
            return {"message": "Request must be JSON"}, 400

        schema = ProductCreateDTO()
        errors = schema.validate(request.json)
        if errors:
            return {"message": str(errors)}, 400

        data = schema.load(request.json)
        product = ProductMapper.to_entity(data)
        ProductRepository.create(product)
        return ProductMapper.to_dto(product), 201


@product_ns.route("/<string:product_id>")
@product_ns.param("product_id", "Product UUID identifier")
class ProductResource(Resource):
    """Single product resource."""

    @product_ns.doc("get_product")
    @product_ns.marshal_with(product_response_model)
    @product_ns.response(200, "Success")
    @product_ns.response(404, "Product not found", error_model)
    def get(self, product_id: str):
        """Get a product by ID."""
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return {"message": "Product not found"}, 404
        return ProductMapper.to_dto(product), 200

    @product_ns.doc("delete_product")
    @product_ns.response(204, "Product deleted")
    @product_ns.response(404, "Product not found", error_model)
    def delete(self, product_id: str):
        """Delete a product by ID."""
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return {"message": "Product not found"}, 404

        ProductRepository.delete(product)
        return "", 204


@product_ns.route("/<string:product_id>/decrease-stock")
@product_ns.param("product_id", "Product UUID identifier")
class ProductDecreaseStock(Resource):
    """Product stock decrease resource."""

    @product_ns.doc("decrease_product_stock")
    @product_ns.expect(decrease_stock_model, validate=False)
    @product_ns.marshal_with(product_response_model)
    @product_ns.response(200, "Stock decreased")
    @product_ns.response(400, "Validation error", error_model)
    @product_ns.response(404, "Product not found", error_model)
    def patch(self, product_id: str):
        """Decrease the quantity of a product."""
        if not request.is_json:
            return {"message": "Request must be JSON"}, 400

        product = ProductRepository.get_by_id(product_id)
        if not product:
            return {"message": "Product not found"}, 404

        schema = ProductDecreaseStockDTO()
        errors = schema.validate(request.json)
        if errors:
            return {"message": str(errors)}, 400

        data = schema.load(request.json)
        quantity = data["quantity"]

        if quantity > product.available_stock:
            return {"message": "Insufficient stock. "
                               f"Available: {product.available_stock}, "
                               f"requested: {quantity}"}, 400

        product = ProductRepository.decrease_stock(product, quantity)
        return ProductMapper.to_dto(product), 200
