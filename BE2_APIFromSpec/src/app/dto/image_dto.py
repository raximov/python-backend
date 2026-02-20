from marshmallow import Schema, fields


class ImageResponseDTO(Schema):
    """DTO for image metadata response."""
    id = fields.String(
        metadata={"description": "Image UUID", "example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    product_id = fields.String(
        metadata={"description": "Associated product UUID"}
    )
