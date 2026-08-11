import uuid

from fastapi import APIRouter, Body, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security.authorization import authorize
from app.services.image_service import ImageService


router = APIRouter(tags=["Images"])


@router.post(
    "/products/{product_id}/image",
    status_code=status.HTTP_201_CREATED,
    summary="Add an image to a product",
)
@authorize
def add_product_image(
    product_id: uuid.UUID,
    image_bytes: bytes = Body(
        ...,
        media_type="application/octet-stream",
    ),
    db: Session = Depends(get_db),
):
    image = ImageService(db).add_to_product(
        product_id=product_id,
        image_bytes=image_bytes,
    )

    return {
        "id": str(image.id),
        "message": "Image added successfully",
    }


@router.put(
    "/images/{image_id}",
    summary="Replace an image",
)
@authorize
def update_image(
    image_id: uuid.UUID,
    image_bytes: bytes = Body(
        ...,
        media_type="application/octet-stream",
    ),
    db: Session = Depends(get_db),
):
    image = ImageService(db).update(
        image_id=image_id,
        image_bytes=image_bytes,
    )

    return {
        "id": str(image.id),
        "message": "Image updated successfully",
    }


@router.get(
    "/images/{image_id}",
    summary="Download image by id",
)
@authorize
def get_image(
    image_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    result = ImageService(db).get_by_id(image_id)

    return Response(
        content=result.image,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{result.id}.bin"'
            ),
            "X-Image-Cache": result.cache_status,
        },
    )


@router.get(
    "/products/{product_id}/image",
    summary="Download product image",
)
@authorize
def get_product_image(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    result = ImageService(db).get_by_product_id(product_id)

    return Response(
        content=result.image,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{result.id}.bin"'
            ),
            "X-Image-Cache": result.cache_status,
        },
    )


@router.delete(
    "/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete image",
)
@authorize
def delete_image(
    image_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    ImageService(db).delete(image_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
