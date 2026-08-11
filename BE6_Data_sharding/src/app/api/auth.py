import json
import secrets
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request as URLRequest
from urllib.request import urlopen

import grpc
from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.dto.auth import (
    LoginDTO,
    OperationDTO,
    RegisterDTO,
    ResetPasswordDTO,
    TokenDTO,
)
from app.grpc.auth_client import auth_grpc_client


router = APIRouter(tags=["Authentication"])


GOOGLE_AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth"
)

GOOGLE_TOKEN_URL = (
    "https://oauth2.googleapis.com/token"
)

GOOGLE_USERINFO_URL = (
    "https://openidconnect.googleapis.com/v1/userinfo"
)

GOOGLE_STATE_COOKIE = "google_oauth_state"


def _handle_grpc_error(exc: grpc.RpcError) -> None:
    code = exc.code()
    detail = exc.details() or "Authorization service error"

    if code == grpc.StatusCode.ALREADY_EXISTS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )

    if code == grpc.StatusCode.UNAUTHENTICATED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

    if code == grpc.StatusCode.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    if code == grpc.StatusCode.INVALID_ARGUMENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    if code == grpc.StatusCode.UNAVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authorization service is unavailable",
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Authorization service error",
    )


def _require_google_config() -> None:
    if not settings.google_client_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GOOGLE_CLIENT_ID is not configured",
        )

    if not settings.google_client_secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GOOGLE_CLIENT_SECRET is not configured",
        )


def _exchange_google_code(code: str) -> str:
    payload = urlencode(
        {
            "code": code,
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": settings.google_redirect_uri,
            "grant_type": "authorization_code",
        }
    ).encode("utf-8")

    request = URLRequest(
        GOOGLE_TOKEN_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": (
                "application/x-www-form-urlencoded"
            ),
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(
            request,
            timeout=settings.google_oauth_timeout_seconds,
        ) as google_response:
            body = json.loads(
                google_response.read().decode("utf-8")
            )

    except HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = "Google token endpoint error"

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Google token exchange failed: {detail}",
        ) from exc

    except (URLError, TimeoutError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Google OAuth service is unavailable",
        ) from exc

    access_token = body.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Google did not return an access token",
        )

    return str(access_token)


def _get_google_userinfo(
    access_token: str,
) -> dict:
    request = URLRequest(
        GOOGLE_USERINFO_URL,
        method="GET",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(
            request,
            timeout=settings.google_oauth_timeout_seconds,
        ) as google_response:
            return json.loads(
                google_response.read().decode("utf-8")
            )

    except HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to obtain Google user information",
        ) from exc

    except (URLError, TimeoutError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Google OAuth service is unavailable",
        ) from exc


@router.post(
    "/register",
    response_model=TokenDTO,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterDTO) -> TokenDTO:
    try:
        response = auth_grpc_client.register(
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            phone_number=payload.phone_number,
            password=payload.password,
        )
    except grpc.RpcError as exc:
        _handle_grpc_error(exc)
        raise

    return TokenDTO(
        access_token=response.access_token,
        token_type=response.token_type,
    )


@router.post(
    "/auth",
    response_model=TokenDTO,
)
def authenticate(payload: LoginDTO) -> TokenDTO:
    try:
        response = auth_grpc_client.login(
            email=payload.email,
            password=payload.password,
        )
    except grpc.RpcError as exc:
        _handle_grpc_error(exc)
        raise

    return TokenDTO(
        access_token=response.access_token,
        token_type=response.token_type,
    )


@router.get(
    "/auth/google/login",
    include_in_schema=True,
)
def google_login() -> RedirectResponse:
    _require_google_config()

    state_value = secrets.token_urlsafe(32)

    query = urlencode(
        {
            "client_id": settings.google_client_id,
            "redirect_uri": settings.google_redirect_uri,
            "response_type": "code",
            "scope": "openid profile email",
            "state": state_value,
            "prompt": "consent",
        }
    )

    response = RedirectResponse(
        url=f"{GOOGLE_AUTH_URL}?{query}",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )

    response.set_cookie(
        key=GOOGLE_STATE_COOKIE,
        value=state_value,
        max_age=600,
        httponly=True,
        secure=settings.google_redirect_uri.startswith(
            "https://"
        ),
        samesite="lax",
    )

    return response


@router.get(
    "/auth/google/callback",
    response_model=TokenDTO,
)
def google_callback(
    request: Request,
    response: Response,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
) -> TokenDTO:
    _require_google_config()

    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Google authorization failed: {error}",
        )

    cookie_state = request.cookies.get(
        GOOGLE_STATE_COOKIE
    )

    if (
        not state
        or not cookie_state
        or not secrets.compare_digest(
            state,
            cookie_state,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Google OAuth state",
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google authorization code is missing",
        )

    access_token = _exchange_google_code(code)

    userinfo = _get_google_userinfo(
        access_token
    )

    google_sub = str(
        userinfo.get("sub") or ""
    ).strip()

    email = str(
        userinfo.get("email") or ""
    ).strip().lower()

    email_verified = userinfo.get(
        "email_verified"
    )

    if (
        not google_sub
        or not email
        or email_verified is not True
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account information is invalid",
        )

    first_name = str(
        userinfo.get("given_name") or ""
    ).strip()

    last_name = str(
        userinfo.get("family_name") or ""
    ).strip()

    try:
        grpc_response = auth_grpc_client.google_login(
            email=email,
            first_name=first_name,
            last_name=last_name,
            google_sub=google_sub,
        )
    except grpc.RpcError as exc:
        _handle_grpc_error(exc)
        raise

    response.delete_cookie(
        GOOGLE_STATE_COOKIE
    )

    return TokenDTO(
        access_token=grpc_response.access_token,
        token_type=grpc_response.token_type,
    )


@router.post(
    "/reset",
    response_model=OperationDTO,
)
def reset_password(
    payload: ResetPasswordDTO,
) -> OperationDTO:
    try:
        grpc_response = (
            auth_grpc_client.reset_password(
                email=payload.email,
            )
        )
    except grpc.RpcError as exc:
        _handle_grpc_error(exc)
        raise

    return OperationDTO(
        success=grpc_response.success,
        message=grpc_response.message,
    )
