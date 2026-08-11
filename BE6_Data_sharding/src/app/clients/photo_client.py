import json
import uuid
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.core.config import settings
from app.core.exceptions import BadRequestError, NotFoundError


@dataclass(frozen=True)
class PhotoResult:
    id: uuid.UUID


class PhotoClient:
    def __init__(
        self,
        base_url: str | None = None,
        timeout: float | None = None,
    ):
        self.base_url = (
            base_url or settings.photo_service_url
        ).rstrip("/")

        self.timeout = (
            timeout
            if timeout is not None
            else settings.photo_service_timeout_seconds
        )

    def _request(
        self,
        method: str,
        path: str,
        body: bytes | None = None,
    ) -> tuple[int, bytes]:
        request = Request(
            url=f"{self.base_url}{path}",
            data=body,
            method=method,
        )

        if body is not None:
            request.add_header(
                "Content-Type",
                "application/octet-stream",
            )

        try:
            with urlopen(
                request,
                timeout=self.timeout,
            ) as response:
                return response.status, response.read()

        except HTTPError as exc:
            error_body = exc.read()

            try:
                payload = json.loads(
                    error_body.decode("utf-8")
                )
                detail = payload.get(
                    "detail",
                    "Photo service error",
                )
            except Exception:
                detail = "Photo service error"

            if exc.code == 404:
                raise NotFoundError(detail) from exc

            if exc.code == 400:
                raise BadRequestError(detail) from exc

            raise BadRequestError(
                f"Photo service returned HTTP {exc.code}"
            ) from exc

        except URLError as exc:
            raise BadRequestError(
                "Photo service is unavailable"
            ) from exc

    def create(
        self,
        image_bytes: bytes,
    ) -> PhotoResult:
        _, body = self._request(
            "POST",
            "/photos",
            body=image_bytes,
        )

        payload = json.loads(body.decode("utf-8"))

        return PhotoResult(
            id=uuid.UUID(payload["id"]),
        )

    def get(
        self,
        photo_id: uuid.UUID,
    ) -> bytes:
        _, body = self._request(
            "GET",
            f"/photos/{photo_id}",
        )

        return body

    def update(
        self,
        photo_id: uuid.UUID,
        image_bytes: bytes,
    ) -> PhotoResult:
        _, body = self._request(
            "PUT",
            f"/photos/{photo_id}",
            body=image_bytes,
        )

        payload = json.loads(body.decode("utf-8"))

        return PhotoResult(
            id=uuid.UUID(payload["id"]),
        )

    def delete(
        self,
        photo_id: uuid.UUID,
    ) -> None:
        self._request(
            "DELETE",
            f"/photos/{photo_id}",
        )
