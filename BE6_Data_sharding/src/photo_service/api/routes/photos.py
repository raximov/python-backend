import uuid

from fastapi import APIRouter, Body, Response, status
from fastapi.responses import JSONResponse

from photo_service.core.exceptions import EmptyPhotoError, PhotoNotFoundError
from photo_service.services.photo_service import PhotoService


router = APIRouter(
    prefix="/photos",
    tags=["Photos"],
)

service = PhotoService()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Upload photo",
)
def create_photo(
    image_bytes: bytes = Body(
        ...,
        media_type="application/octet-stream",
    ),
):
    try:
        photo = service.create(image_bytes)
    except EmptyPhotoError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    return {
        "id": str(photo.id),
        "message": "Photo created successfully",
    }


@router.get(
    "/{photo_id}",
    summary="Download photo",
)
def get_photo(photo_id: uuid.UUID):
    try:
        photo = service.get_by_id(photo_id)
    except PhotoNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    return Response(
        content=photo.image,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{photo.id}.bin"'
            ),
        },
    )


@router.put(
    "/{photo_id}",
    summary="Replace photo",
)
def update_photo(
    photo_id: uuid.UUID,
    image_bytes: bytes = Body(
        ...,
        media_type="application/octet-stream",
    ),
):
    try:
        photo = service.update(
            photo_id=photo_id,
            image_bytes=image_bytes,
        )
    except EmptyPhotoError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )
    except PhotoNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    return {
        "id": str(photo.id),
        "message": "Photo updated successfully",
    }


@router.delete(
    "/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete photo",
)
def delete_photo(photo_id: uuid.UUID):
    try:
        service.delete(photo_id)
    except PhotoNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
