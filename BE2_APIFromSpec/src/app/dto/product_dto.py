from marshmallow import Schema, fields, validate


class ProductCreateDTO(Schema):
    """DTO for creating a product."""
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=200),
        metadata={"description": "Product name", "example": "Washing Machine X200"}
    )
    category = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        metadata={"description": "Product category", "example": "Washing Machines"}
    )
    price = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        metadata={"description": "Product price", "example": 29999.99}
    )
    available_stock = fields.Integer(
        required=False,
        load_default=0,
        validate=validate.Range(min=0),
        metadata={"description": "Available stock quantity", "example": 50}
    )
    supplier_id = fields.String(
        required=False,
        load_default=None,
        metadata={"description": "Supplier UUID", "example": "550e8400-e29b-41d4-a716-446655440000"}
    )


class ProductResponseDTO(Schema):
    """DTO for product response."""
    id = fields.String(
        metadata={"description": "Product UUID", "example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    name = fields.String(
        metadata={"description": "Product name", "example": "Washing Machine X200"}
    )
    category = fields.String(
        metadata={"description": "Product category", "example": "Washing Machines"}
    )
    price = fields.Float(
        metadata={"description": "Product price", "example": 29999.99}
    )
    available_stock = fields.Integer(
        metadata={"description": "Available stock quantity", "example": 50}
    )
    last_update_date = fields.DateTime(
        metadata={"description": "Last update timestamp"}
    )
    supplier_id = fields.String(
        metadata={"description": "Supplier UUID"}
    )
    image_id = fields.String(
        metadata={"description": "Image UUID"}
    )


class ProductDecreaseStockDTO(Schema):
    """DTO for decreasing product stock."""
    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1),
        metadata={"description": "Quantity to decrease", "example": 5}
    )
