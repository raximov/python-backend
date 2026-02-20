from flask import request
from flask_restx import Namespace, Resource, fields

from app.dto.supplier_dto import SupplierCreateDTO, SupplierUpdateAddressDTO
from app.dto.address_dto import AddressCreateDTO
from app.mappers.supplier_mapper import SupplierMapper
from app.mappers.address_mapper import AddressMapper
from app.repositories.supplier_repository import SupplierRepository
from app.repositories.address_repository import AddressRepository

supplier_ns = Namespace("Suppliers", description="Supplier management operations")

# ---- Swagger Models ----
address_model = supplier_ns.model("SupplierAddress", {
    "id": fields.String(readonly=True, description="Address UUID"),
    "country": fields.String(required=True, description="Country name", example="Russia"),
    "city": fields.String(required=True, description="City name", example="Moscow"),
    "street": fields.String(required=True, description="Street address", example="Tverskaya 1"),
})

address_input_model = supplier_ns.model("SupplierAddressInput", {
    "country": fields.String(required=True, description="Country name", example="Russia"),
    "city": fields.String(required=True, description="City name", example="Moscow"),
    "street": fields.String(required=True, description="Street address", example="Tverskaya 1"),
})

supplier_input_model = supplier_ns.model("SupplierInput", {
    "name": fields.String(required=True, description="Supplier name",
                          example="TechSupply Co."),
    "phone_number": fields.String(description="Phone number",
                                  example="+7-999-123-4567"),
    "address": fields.Nested(address_input_model, description="Supplier address",
                             required=False),
})

supplier_response_model = supplier_ns.model("SupplierResponse", {
    "id": fields.String(readonly=True, description="Supplier UUID",
                        example="550e8400-e29b-41d4-a716-446655440000"),
    "name": fields.String(description="Supplier name", example="TechSupply Co."),
    "phone_number": fields.String(description="Phone number",
                                  example="+7-999-123-4567"),
    "address": fields.Nested(address_model, description="Supplier address",
                             allow_null=True),
})

error_model = supplier_ns.model("SupplierError", {
    "message": fields.String(description="Error message"),
})


@supplier_ns.route("")
class SupplierList(Resource):
    """Supplier collection resource."""

    @supplier_ns.doc("get_all_suppliers")
    @supplier_ns.marshal_list_with(supplier_response_model)
    @supplier_ns.response(200, "Success")
    def get(self):
        """Get all suppliers."""
        suppliers = SupplierRepository.get_all()
        return [SupplierMapper.to_dto(s) for s in suppliers], 200

    @supplier_ns.doc("create_supplier")
    @supplier_ns.expect(supplier_input_model, validate=False)
    @supplier_ns.marshal_with(supplier_response_model, code=201)
    @supplier_ns.response(400, "Validation error", error_model)
    @supplier_ns.response(201, "Supplier created")
    def post(self):
        """Add a new supplier."""
        if not request.is_json:
            return {"message": "Request must be JSON"}, 400

        schema = SupplierCreateDTO()
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

        supplier = SupplierMapper.to_entity(data)
        if address:
            supplier.address_id = address.id
            supplier.address = address

        SupplierRepository.create(supplier)
        return SupplierMapper.to_dto(supplier), 201


@supplier_ns.route("/<string:supplier_id>")
@supplier_ns.param("supplier_id", "Supplier UUID identifier")
class SupplierResource(Resource):
    """Single supplier resource."""

    @supplier_ns.doc("get_supplier")
    @supplier_ns.marshal_with(supplier_response_model)
    @supplier_ns.response(200, "Success")
    @supplier_ns.response(404, "Supplier not found", error_model)
    def get(self, supplier_id: str):
        """Get a supplier by ID."""
        supplier = SupplierRepository.get_by_id(supplier_id)
        if not supplier:
            return {"message": "Supplier not found"}, 404
        return SupplierMapper.to_dto(supplier), 200

    @supplier_ns.doc("delete_supplier")
    @supplier_ns.response(204, "Supplier deleted")
    @supplier_ns.response(404, "Supplier not found", error_model)
    def delete(self, supplier_id: str):
        """Delete a supplier by ID."""
        supplier = SupplierRepository.get_by_id(supplier_id)
        if not supplier:
            return {"message": "Supplier not found"}, 404

        SupplierRepository.delete(supplier)
        return "", 204


@supplier_ns.route("/<string:supplier_id>/address")
@supplier_ns.param("supplier_id", "Supplier UUID identifier")
class SupplierAddress(Resource):
    """Supplier address update resource."""

    @supplier_ns.doc("update_supplier_address")
    @supplier_ns.expect(address_input_model, validate=False)
    @supplier_ns.marshal_with(supplier_response_model)
    @supplier_ns.response(200, "Address updated")
    @supplier_ns.response(400, "Validation error", error_model)
    @supplier_ns.response(404, "Supplier not found", error_model)
    def patch(self, supplier_id: str):
        """Change supplier address."""
        if not request.is_json:
            return {"message": "Request must be JSON"}, 400

        supplier = SupplierRepository.get_by_id(supplier_id)
        if not supplier:
            return {"message": "Supplier not found"}, 404

        schema = SupplierUpdateAddressDTO()
        errors = schema.validate(request.json)
        if errors:
            return {"message": str(errors)}, 400

        data = schema.load(request.json)

        if supplier.address:
            supplier.address.country = data["country"]
            supplier.address.city = data["city"]
            supplier.address.street = data["street"]
            AddressRepository.update(supplier.address)
        else:
            address = AddressMapper.to_entity(data)
            AddressRepository.create(address)
            supplier.address_id = address.id
            supplier.address = address
            SupplierRepository.update(supplier)

        return SupplierMapper.to_dto(supplier), 200
