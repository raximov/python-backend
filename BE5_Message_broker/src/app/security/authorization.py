from collections.abc import Callable
from typing import Any, TypeVar


F = TypeVar("F", bound=Callable[..., Any])

_AUTHORIZATION_ATTRIBUTE = "__authorization_required__"


def authorize(func: F) -> F:
    """Mark a controller method as requiring authorization."""
    setattr(func, _AUTHORIZATION_ATTRIBUTE, True)
    return func


def requires_authorization(endpoint: Callable[..., Any] | None) -> bool:
    if endpoint is None:
        return False

    return bool(
        getattr(
            endpoint,
            _AUTHORIZATION_ATTRIBUTE,
            False,
        )
    )
