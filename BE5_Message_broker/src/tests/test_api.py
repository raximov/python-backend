import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _unique_phone() -> str:
    """Generate a valid unique Uzbek-style phone number for tests."""
    suffix = uuid.uuid4().int % 1_000_000_000
    return f"+998{suffix:09d}"


@pytest.fixture
def authorized_client() -> TestClient:
    """
    Create a real authorization user through /register,
    obtain JWT and return an authenticated TestClient.
    """
    test_client = TestClient(app)

    unique = uuid.uuid4().hex

    response = test_client.post(
        "/register",
        json={
            "email": f"pytest.{unique}@example.com",
            "first_name": "Pytest",
            "last_name": "User",
            "phone_number": _unique_phone(),
            "password": "PytestPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["token_type"] == "bearer"
    assert data["access_token"]

    test_client.headers.update(
        {
            "Authorization": (
                f"Bearer {data['access_token']}"
            )
        }
    )

    return test_client


def test_health_and_documentation():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ShopAPI",
    }

    response = client.get("/swagger/index.html")
    assert response.status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_public_auth_flow():
    """
    /register, /auth and /reset must remain public.
    """
    public_client = TestClient(app)

    unique = uuid.uuid4().hex
    email = f"auth-test.{unique}@example.com"
    password = "AuthTestPassword123!"

    # REGISTER
    response = public_client.post(
        "/register",
        json={
            "email": email,
            "first_name": "Auth",
            "last_name": "Test",
            "phone_number": _unique_phone(),
            "password": password,
        },
    )

    assert response.status_code == 201
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]

    # LOGIN
    response = public_client.post(
        "/auth",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]

    # WRONG PASSWORD
    response = public_client.post(
        "/auth",
        json={
            "email": email,
            "password": "WRONG_PASSWORD",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password"
    }

    # RESET PASSWORD
    response = public_client.post(
        "/reset",
        json={
            "email": email,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Password reset successfully",
    }


def test_full_shop_api_flow(
    authorized_client: TestClient,
):
    client = authorized_client
    unique = uuid.uuid4().hex[:8]

    # =========================
    # 1. SUPPLIER CREATE
    # =========================
    response = client.post(
        "/api/v1/suppliers",
        json={
            "name": f"Test Supplier {unique}",
            "phone_number": _unique_phone(),
            "address": {
                "country": "Uzbekistan",
                "city": "Tashkent",
                "street": "Test Street 1",
            },
        },
    )

    assert response.status_code == 201

    supplier = response.json()
    supplier_id = supplier["id"]

    # =========================
    # 2. SUPPLIER GET BY ID
    # =========================
    response = client.get(
        f"/api/v1/suppliers/{supplier_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == supplier_id

    # =========================
    # 3. SUPPLIER ADDRESS UPDATE
    # =========================
    response = client.patch(
        f"/api/v1/suppliers/{supplier_id}/address",
        json={
            "country": "Uzbekistan",
            "city": "Samarkand",
            "street": "Registan 10",
        },
    )

    assert response.status_code == 200
    assert response.json()["address"]["city"] == "Samarkand"

    # =========================
    # 4. CLIENT CREATE
    # =========================
    response = client.post(
        "/api/v1/clients",
        json={
            "client_name": f"Habibjon{unique}",
            "client_surname": "Kadirov",
            "birthday": "2004-05-10",
            "gender": "male",
            "address": {
                "country": "Uzbekistan",
                "city": "Tashkent",
                "street": "Yunusobod 10",
            },
        },
    )

    assert response.status_code == 201

    created_client = response.json()
    client_id = created_client["id"]

    # =========================
    # 5. CLIENT SEARCH
    # =========================
    response = client.get(
        "/api/v1/clients/search",
        params={
            "name": f"Habibjon{unique}",
            "surname": "Kadirov",
        },
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1

    # =========================
    # 6. CLIENT PAGINATION
    # =========================
    response = client.get(
        "/api/v1/clients",
        params={
            "limit": 1,
            "offset": 0,
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 1

    # =========================
    # 7. CLIENT ADDRESS UPDATE
    # =========================
    response = client.patch(
        f"/api/v1/clients/{client_id}/address",
        json={
            "country": "Uzbekistan",
            "city": "Bukhara",
            "street": "Old City 20",
        },
    )

    assert response.status_code == 200
    assert response.json()["address"]["city"] == "Bukhara"

    # =========================
    # 8. PRODUCT CREATE
    # =========================
    response = client.post(
        "/api/v1/products",
        json={
            "name": f"Samsung TV {unique}",
            "category": "Television",
            "price": 8500000,
            "available_stock": 10,
            "supplier_id": supplier_id,
        },
    )

    assert response.status_code == 201

    product = response.json()
    product_id = product["id"]

    assert product["available_stock"] == 10

    # =========================
    # 9. PRODUCT GET BY ID
    # =========================
    response = client.get(
        f"/api/v1/products/{product_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == product_id

    # =========================
    # 10. AVAILABLE PRODUCTS
    # =========================
    response = client.get(
        "/api/v1/products/available"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # =========================
    # 11. STOCK DECREASE
    # =========================
    response = client.patch(
        f"/api/v1/products/{product_id}/stock",
        json={
            "quantity": 3,
        },
    )

    assert response.status_code == 200
    assert response.json()["available_stock"] == 7

    # =========================
    # 12. STOCK ERROR
    # =========================
    response = client.patch(
        f"/api/v1/products/{product_id}/stock",
        json={
            "quantity": 100,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Not enough product in stock"
    )

    # =========================
    # 13. IMAGE CREATE
    # =========================
    first_image = b"school21-test-image-v1"

    response = client.post(
        f"/api/v1/products/{product_id}/image",
        content=first_image,
        headers={
            "Content-Type": "application/octet-stream",
        },
    )

    assert response.status_code == 201

    image_id = response.json()["id"]

    # =========================
    # 14. IMAGE GET BY ID
    # =========================
    response = client.get(
        f"/api/v1/images/{image_id}"
    )

    assert response.status_code == 200
    assert response.content == first_image

    assert (
        response.headers["content-type"]
        == "application/octet-stream"
    )

    assert (
        "attachment"
        in response.headers["content-disposition"]
    )

    # =========================
    # 15. IMAGE GET BY PRODUCT
    # =========================
    response = client.get(
        f"/api/v1/products/{product_id}/image"
    )

    assert response.status_code == 200
    assert response.content == first_image

    # =========================
    # 16. IMAGE UPDATE
    # =========================
    second_image = b"school21-test-image-v2"

    response = client.put(
        f"/api/v1/images/{image_id}",
        content=second_image,
        headers={
            "Content-Type": "application/octet-stream",
        },
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/v1/images/{image_id}"
    )

    assert response.status_code == 200
    assert response.content == second_image

    # =========================
    # 17. IMAGE DELETE
    # =========================
    response = client.delete(
        f"/api/v1/images/{image_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/images/{image_id}"
    )

    assert response.status_code == 404

    # =========================
    # 18. PRODUCT DELETE
    # =========================
    response = client.delete(
        f"/api/v1/products/{product_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/v1/products/{product_id}"
    )

    assert response.status_code == 404

    # =========================
    # 19. CLIENT DELETE
    # =========================
    response = client.delete(
        f"/api/v1/clients/{client_id}"
    )

    assert response.status_code == 204

    # =========================
    # 20. SUPPLIER DELETE
    # =========================
    response = client.delete(
        f"/api/v1/suppliers/{supplier_id}"
    )

    assert response.status_code == 204


def test_invalid_request_returns_400(
    authorized_client: TestClient,
):
    client = authorized_client

    response = client.post(
        "/api/v1/products",
        json={
            "name": "Invalid TV",
            "category": "TV",
            "price": -100,
            "available_stock": -5,
            "supplier_id": (
                "11111111-1111-1111-1111-111111111111"
            ),
        },
    )

    assert response.status_code == 400


def test_not_found_returns_404(
    authorized_client: TestClient,
):
    client = authorized_client

    missing_id = (
        "11111111-1111-1111-1111-111111111111"
    )

    response = client.get(
        f"/api/v1/suppliers/{missing_id}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Supplier not found"
    }


def test_protected_endpoint_requires_token():
    public_client = TestClient(app)

    response = public_client.get(
        "/api/v1/products/available"
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Authorization header is required"
    }


def test_protected_endpoint_rejects_invalid_token():
    public_client = TestClient(app)

    response = public_client.get(
        "/api/v1/products/available",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or expired token"
    }