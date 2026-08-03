class AuthError(Exception):
    pass


class UserAlreadyExistsError(AuthError):
    pass


class UserNotFoundError(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass


class InvalidTokenError(AuthError):
    pass


class InvalidInputError(AuthError):
    pass
