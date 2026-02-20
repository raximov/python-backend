from marshmallow import Schema, fields, validate


class SupplierCreateDTO(Schema):
    """DTO for creating a supplier."""
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=150),
        metadata={"description": "Supplier name", "example": "TechSupply Co."}
    )
    phone_number = fields.String(
        required=False,
        load_default=None,
        validate=validate.Length(max=20),
        metadata={"description": "Phone number", "example": "+7-999-123-4567"}
    )
    address = fields.Nested(
        "AddressCreateDTO",
        required=False,
        load_default=None,
        metadata={"description": "Supplier address"}
    )


class SupplierResponseDTO(Schema):
    """DTO for supplier response."""
    id = fields.String(
        metadata={"description": "Supplier UUID", "example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    name = fields.String(
        metadata={"description": "Supplier name", "example": "TechSupply Co."}
    )
    phone_number = fields.String(
        metadata={"description": "Phone number", "example": "+7-999-123-4567"}
    )
    address = fields.Nested(
        "AddressResponseDTO",
        metadata={"description": "Supplier address"}
    )


class SupplierUpdateAddressDTO(Schema):
    """DTO for updating supplier address."""
    country = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        metadata={"description": "Country name", "example": "Russia"}
    )
    city = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        metadata={"description": "City name", "example": "Moscow"}
    )
    street = fields.String(
        required=True,
        validate=validate.Length(min=1, max=255),
        metadata={"description": "Street address", "example": "Tverskaya 1"}
    )
