import io

from flask import request, send_file
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage

from app import db
from app.models.image import Image
from app.models.product import Product
from app.repositories.image_repository import ImageRepository
from app.repositories.product_repository import ProductRepository

image_ns = Namespace("Images", description="Image management operations")

# ---- Swagger Models ----
image_upload_parser = image_ns.parser()
image_upload_parser.add_argument(
    "image", location="files", type=FileStorage, required=True,
    help="Image file to upload"
)
image_upload_parser.add_argument(
    "product_id", location="form", type=str, required=True,
    help="Product UUID to associate the image with"
)

image_replace_parser = image_ns.parser()
image_replace_parser.add_argument(
    "image", location="files", type=FileStorage, required=True,
    help="New image file to replace the existing one"
)

image_meta_model = image_ns.model("ImageMeta", {
    "id": fields.String(readonly=True, description="Image UUID",
                        example="550e8400-e29b-41d4-a716-446655440000"),
    "product_id": fields.String(description="Associated product UUID"),
})

error_model = image_ns.model("ImageError", {
    "message": fields.String(description="Error message"),
})


@image_ns.route("")
class ImageUpload(Resource):
    """Image upload resource."""

    @image_ns.doc("upload_image")
    @image_ns.expect(image_upload_parser, validate=False)
    @image_ns.marshal_with(image_meta_model, code=201)
    @image_ns.response(400, "Validation error", error_model)
    @image_ns.response(404, "Product not found", error_model)
    @image_ns.response(201, "Image uploaded")
    def post(self):
        """Add an image (byte array of the image and the product id)."""
        args = image_upload_parser.parse_args()
        image_file = args.get("image")
        product_id = args.get("product_id")

        if not image_file:
            return {"message": "Image file is required"}, 400
        if not product_id:
            return {"message": "product_id is required"}, 400

        # Verify product exists
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return {"message": "Product not found"}, 404

        # Read image bytes
        image_data = image_file.read()
        if not image_data:
            return {"message": "Image file is empty"}, 400

        # Create image record
        image = Image(image=image_data)
        ImageRepository.create(image)

        # Link image to product
        product.image_id = image.id
        ProductRepository.update(product)

        return {"id": image.id, "product_id": product_id}, 201


@image_ns.route("/<string:image_id>")
@image_ns.param("image_id", "Image UUID identifier")
class ImageResource(Resource):
    """Single image resource."""

    @image_ns.doc("get_image_by_id")
    @image_ns.response(200, "Image binary data (application/octet-stream)")
    @image_ns.response(404, "Image not found", error_model)
    def get(self, image_id: str):
        """Get an image by image ID. Returns binary data with application/octet-stream header."""
        image = ImageRepository.get_by_id(image_id)
        if not image:
            return {"message": "Image not found"}, 404

        return send_file(
            io.BytesIO(image.image),
            mimetype="application/octet-stream",
            as_attachment=True,
            download_name=f"{image.id}.bin",
        )

    @image_ns.doc("replace_image")
    @image_ns.expect(image_replace_parser, validate=False)
    @image_ns.marshal_with(image_meta_model)
    @image_ns.response(200, "Image replaced")
    @image_ns.response(400, "Validation error", error_model)
    @image_ns.response(404, "Image not found", error_model)
    def put(self, image_id: str):
        """Replace an image (the image ID and a new file to replace)."""
        image = ImageRepository.get_by_id(image_id)
        if not image:
            return {"message": "Image not found"}, 404

        args = image_replace_parser.parse_args()
        image_file = args.get("image")

        if not image_file:
            return {"message": "Image file is required"}, 400

        image_data = image_file.read()
        if not image_data:
            return {"message": "Image file is empty"}, 400

        image.image = image_data
        ImageRepository.update(image)

        # Find associated product
        product = Product.query.filter_by(image_id=image_id).first()
        product_id = product.id if product else None

        return {"id": image.id, "product_id": product_id}, 200

    @image_ns.doc("delete_image")
    @image_ns.response(204, "Image deleted")
    @image_ns.response(404, "Image not found", error_model)
    def delete(self, image_id: str):
        """Delete an image by image ID."""
        image = ImageRepository.get_by_id(image_id)
        if not image:
            return {"message": "Image not found"}, 404

        # Unlink from any associated products
        products = Product.query.filter_by(image_id=image_id).all()
        for product in products:
            product.image_id = None
        db.session.commit()

        ImageRepository.delete(image)
        return "", 204


@image_ns.route("/product/<string:product_id>")
@image_ns.param("product_id", "Product UUID identifier")
class ImageByProduct(Resource):
    """Image by product resource."""

    @image_ns.doc("get_image_by_product")
    @image_ns.response(200, "Image binary data (application/octet-stream)")
    @image_ns.response(404, "Image or product not found", error_model)
    def get(self, product_id: str):
        """Get an image of a specific product (by product ID). Returns binary with application/octet-stream."""
        product = ProductRepository.get_by_id(product_id)
        if not product:
            return {"message": "Product not found"}, 404

        if not product.image_id:
            return {"message": "No image associated with this product"}, 404

        image = ImageRepository.get_by_id(product.image_id)
        if not image:
            return {"message": "Image not found"}, 404

        return send_file(
            io.BytesIO(image.image),
            mimetype="application/octet-stream",
            as_attachment=True,
            download_name=f"{image.id}.bin",
        )
