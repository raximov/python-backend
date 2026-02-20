from flask import request
from flask_restx import Namespace, Resource, fields

from app.dto.client_dto import ClientCreateDTO, ClientResponseDTO, ClientUpdateAddressDTO
from app.dto.address_dto import AddressCreateDTO
from app.mappers.client_mapper import ClientMapper
from app.mappers.address_mapper import AddressMapper
from app.repositories.client_repository import ClientRepository
from app.repositories.address_repository import AddressRepository

client_ns = Namespace("Clients", description="Client management operations")

# ---- Swagger Models ----
address_model = client_ns.model("Address", {
    "id": fields.String(readonly=True, description="Address UUID",
                        example="550e8400-e29b-41d4-a716-446655440000"),
    "country": fields.String(required=True, description="Country name", example="Russia"),
    "city": fields.String(required=True, description="City name", example="Moscow"),
    "street": fields.String(required=True, description="Street address", example="Tverskaya 1"),
})

address_input_model = client_ns.model("AddressInput", {
    "country": fields.String(required=True, description="Country name", example="Russia"),
    "city": fields.String(required=True, description="City name", example="Moscow"),
    "street": fields.String(required=True, description="Street address", example="Tverskaya 1"),
})

client_input_model = client_ns.model("ClientInput", {
    "client_name": fields.String(required=True, description="Client first name", example="Ivan"),
    "client_surname": fields.String(required=True, description="Client last name", example="Ivanov"),
    "birthday": fields.Date(description="Client birthday (YYYY-MM-DD)", example="1990-01-15"),
    "gender": fields.String(description="Gender (male/female/other)", example="male",
                            enum=["male", "female", "other"]),
    "address": fields.Nested(address_input_model, description="Client address", required=False),
})

client_response_model = client_ns.model("ClientResponse", {
    "id": fields.String(readonly=True, description="Client UUID",
                        example="550e8400-e29b-41d4-a716-446655440000"),
    "client_name": fields.String(description="Client first name", example="Ivan"),
    "client_surname": fields.String(description="Client last name", example="Ivanov"),
    "birthday": fields.Date(description="Client birthday", example="1990-01-15"),
    "gender": fields.String(description="Gender", example="male"),
    "registration_date": fields.DateTime(description="Registration timestamp"),
    "address": fields.Nested(address_model, description="Client address", allow_null=True),
})

error_model = client_ns.model("Error", {
    "message": fields.String(description="Error message"),
})


@client_ns.route("")
class ClientList(Resource):
    """Client collection resource."""

    @client_ns.doc("get_all_clients",
                   params={
                       "limit": {"description": "Max number of results", "type": "integer", "required": False},
                       "offset": {"description": "Number of results to skip", "type": "integer", "required": False},
                   })
    @client_ns.marshal_list_with(client_response_model)
    @client_ns.response(200, "Success")
    def get(self):
        """Get all clients with optional pagination (limit & offset)."""
        limit = request.args.get("limit", default=None, type=int)
        offset = request.args.get("offset", default=None, type=int)

        clients = ClientRepository.get_all(limit=limit, offset=offset)
        return [ClientMapper.to_dto(c) for c in clients], 200

    @client_ns.doc("create_client")
    @client_ns.expect(client_input_model, validate=False)
    @client_ns.marshal_with(client_response_model, code=201)
    @client_ns.response(400, "Validation error", error_model)
    @client_ns.response(201, "Client created")
    def post(self):
        """Add a new client."""
        if not request.is_json:
            return {"message": "Request must be JSON"}, 400

        schema = ClientCreateDTO()
        errors = schema.validate(request.json)
        if errors:
            return {"message": str(errors)}, 400

        data = schema.load(request.json)

        # Handle nested address
        address = None
        if data.get("address"):
            address_schema = AddressCreateDTO()
            addr_errors = address_schema.validate(data["address"])
            if addr_errors:
                return {"message": str(addr_errors)}, 400
            address = AddressMapper.to_entity(data["address"])
            AddressRepository.create(address)

        client = ClientMapper.to_entity(data)
        if address:
            client.address_id = address.id
            client.address = address

        ClientRepository.create(client)
        return ClientMapper.to_dto(client), 201


@client_ns.route("/<string:client_id>")
@client_ns.param("client_id", "Client UUID identifier")
class ClientResource(Resource):
    """Single client resource."""

    @client_ns.doc("delete_client")
    @client_ns.response(204, "Client deleted")
    @client_ns.response(404, "Client not found", error_model)
    def delete(self, client_id: str):
        """Delete a client by ID."""
        client = ClientRepository.get_by_id(client_id)
        if not client:
            return {"message": "Client not found"}, 404

        ClientRepository.delete(client)
        return "", 204


@client_ns.route("/search")
class ClientSearch(Resource):
    """Client search resource."""

    @client_ns.doc("search_clients",
                   params={
                       "client_name": {"description": "First name to search", "type": "string", "required": False},
                       "client_surname": {"description": "Last name to search", "type": "string", "required": False},
                   })
    @client_ns.marshal_list_with(client_response_model)
    @client_ns.response(200, "Success")
    def get(self):
        """Search clients by first and last name."""
        client_name = request.args.get("client_name", default="", type=str)
        client_surname = request.args.get("client_surname", default="", type=str)

        clients = ClientRepository.get_by_name(client_name, client_surname)
        return [ClientMapper.to_dto(c) for c in clients], 200


@client_ns.route("/<string:client_id>/address")
@client_ns.param("client_id", "Client UUID identifier")
class ClientAddress(Resource):
    """Client address update resource."""

    @client_ns.doc("update_client_address")
    @client_ns.expect(address_input_model, validate=False)
    @client_ns.marshal_with(client_response_model)
    @client_ns.response(200, "Address updated")
    @client_ns.response(400, "Validation error", error_model)
    @client_ns.response(404, "Client not found", error_model)
    def patch(self, client_id: str):
        """Change client address."""
        if not request.is_json:
            return {"message": "Request must be JSON"}, 400

        client = ClientRepository.get_by_id(client_id)
        if not client:
            return {"message": "Client not found"}, 404

        schema = ClientUpdateAddressDTO()
        errors = schema.validate(request.json)
        if errors:
            return {"message": str(errors)}, 400

        data = schema.load(request.json)

        if client.address:
            # Update existing address
            client.address.country = data["country"]
            client.address.city = data["city"]
            client.address.street = data["street"]
            AddressRepository.update(client.address)
        else:
            # Create new address
            address = AddressMapper.to_entity(data)
            AddressRepository.create(address)
            client.address_id = address.id
            client.address = address
            ClientRepository.update(client)

        return ClientMapper.to_dto(client), 200
