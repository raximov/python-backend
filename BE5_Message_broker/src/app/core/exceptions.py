class BadRequestError(Exception):
    """Request data is valid syntactically, but cannot be processed."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(Exception):
    """Requested resource does not exist."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)