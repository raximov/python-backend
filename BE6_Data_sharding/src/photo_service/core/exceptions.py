class PhotoServiceError(Exception):
    pass


class PhotoNotFoundError(PhotoServiceError):
    pass


class EmptyPhotoError(PhotoServiceError):
    pass
