from marshmallow import Schema, fields, validate


class ClientCreateDTO(Schema):
    """DTO for creating a client."""
    client_name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        metadata={"description": "Client first name", "example": "Ivan"}
    )
    client_surname = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        metadata={"description": "Client last name", "example": "Ivanov"}
    )
    birthday = fields.Date(
        required=False,
        load_default=None,
        metadata={"description": "Client birthday", "example": "1990-01-15"}
    )
    gender = fields.String(
        required=False,
        load_default=None,
        validate=validate.OneOf(["male", "female", "other"]),
        metadata={"description": "Client gender", "example": "male"}
    )
    address = fields.Nested(
        "AddressCreateDTO",
        required=False,
        load_default=None,
        metadata={"description": "Client address"}
    )


class ClientResponseDTO(Schema):
    """DTO for client response."""
    id = fields.String(
        metadata={"description": "Client UUID", "example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    client_name = fields.String(
        metadata={"description": "Client first name", "example": "Ivan"}
    )
    client_surname = fields.String(
        metadata={"description": "Client last name", "example": "Ivanov"}
    )
    birthday = fields.Date(
        metadata={"description": "Client birthday", "example": "1990-01-15"}
    )
    gender = fields.String(
        metadata={"description": "Client gender", "example": "male"}
    )
    registration_date = fields.DateTime(
        metadata={"description": "Registration timestamp"}
    )
    address = fields.Nested(
        "AddressResponseDTO",
        metadata={"description": "Client address"}
    )


class ClientUpdateAddressDTO(Schema):
    """DTO for updating client address."""
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
