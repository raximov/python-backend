from collections.abc import Callable
from typing import Any

import grpc
from fastapi.routing import iter_route_contexts
from starlette.concurrency import run_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Match

from app.grpc.auth_client import auth_grpc_client
from app.security.authorization import requires_authorization


def _find_endpoint(request: Request) -> Callable[..., Any] | None:
    for route in iter_route_contexts(request.app.routes):
        match, child_scope = route.matches(request.scope)

        if match != Match.FULL:
            continue

        endpoint = child_scope.get("endpoint")

        if endpoint is not None:
            return endpoint

        matched_route = child_scope.get("route")
        return getattr(matched_route, "endpoint", None)

    return None


def _unauthorized(detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": detail},
        headers={"WWW-Authenticate": "Bearer"},
    )


class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        endpoint = _find_endpoint(request)

        # Public controller: authentication is not required.
        if not requires_authorization(endpoint):
            return await call_next(request)

        authorization = request.headers.get("Authorization")

        if not authorization:
            return _unauthorized("Authorization header is required")

        scheme, separator, token = authorization.partition(" ")

        if (
            not separator
            or scheme.lower() != "bearer"
            or not token.strip()
        ):
            return _unauthorized(
                "Authorization header must use Bearer token"
            )

        try:
            result = await run_in_threadpool(
                auth_grpc_client.validate_token,
                token.strip(),
            )
        except grpc.RpcError as exc:
            if exc.code() == grpc.StatusCode.UNAUTHENTICATED:
                return _unauthorized("Invalid or expired token")

            if exc.code() == grpc.StatusCode.UNAVAILABLE:
                return JSONResponse(
                    status_code=503,
                    content={
                        "detail": "Authorization service is unavailable"
                    },
                )

            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Authorization service error"
                },
            )

        if not result.valid:
            return _unauthorized("Invalid or expired token")

        request.state.user_id = result.user_id
        request.state.user_email = result.email

        return await call_next(request)
