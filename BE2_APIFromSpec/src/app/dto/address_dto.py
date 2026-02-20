from marshmallow import Schema, fields, validate


class AddressCreateDTO(Schema):
    """DTO for creating an address."""
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


class AddressResponseDTO(Schema):
    """DTO for address response."""
    id = fields.String(
        metadata={"description": "Address UUID", "example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    country = fields.String(
        metadata={"description": "Country name", "example": "Russia"}
    )
    city = fields.String(
        metadata={"description": "City name", "example": "Moscow"}
    )
    street = fields.String(
        metadata={"description": "Street address", "example": "Tverskaya 1"}
    )
