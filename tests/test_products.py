"""Automated test suite for Product Management API endpoints.

Tests all CRUD operations, edge cases, error handling, and input validation
while ensuring full test isolation via an autouse fixture.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import product_store


@pytest.fixture(autouse=True)
def isolate_store() -> Generator[None, None, None]:
    """Isolate tests by clearing the in-memory product store before and after each test.

    Ensures that test execution order does not affect results.
    """
    product_store.clear()
    yield
    product_store.clear()


@pytest.fixture
def client() -> TestClient:
    """Create a test client instance connected to the FastAPI application."""
    return TestClient(app)


# ============================================================================
# Root and Health Endpoints
# ============================================================================


def test_root_welcome(client: TestClient) -> None:
    """Test that GET / returns the welcome message, docs link, and version."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs_url" in data
    assert data["docs_url"] == "/docs"
    assert data["version"] == "1.0.0"


def test_health_check(client: TestClient) -> None:
    """Test that GET /health returns service status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "healthy", "service": "product-api"}


# ============================================================================
# Product Creation (POST /products)
# ============================================================================


def test_create_product_success(client: TestClient) -> None:
    """Test successful creation of a product with all fields."""
    payload = {
        "name": "Wireless Mouse",
        "description": "Ergonomic 2.4GHz optical mouse",
        "price": 29.99,
        "in_stock": True,
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Wireless Mouse"
    assert data["description"] == "Ergonomic 2.4GHz optical mouse"
    assert data["price"] == 29.99
    assert data["in_stock"] is True


def test_create_product_minimal_fields(client: TestClient) -> None:
    """Test creating a product with only required fields (description omitted)."""
    payload = {
        "name": "USB-C Cable",
        "price": 9.99,
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "USB-C Cable"
    assert data["description"] is None
    assert data["price"] == 9.99
    assert data["in_stock"] is True  # Default value


def test_create_product_empty_name(client: TestClient) -> None:
    """Test validation failure when product name is empty."""
    payload = {"name": "", "price": 19.99}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_product_whitespace_only_name(client: TestClient) -> None:
    """Test validation failure when product name is only whitespace."""
    payload = {"name": "     ", "price": 19.99}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_product_zero_price(client: TestClient) -> None:
    """Test validation failure when price is zero."""
    payload = {"name": "Free Sample", "price": 0.0}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_product_negative_price(client: TestClient) -> None:
    """Test validation failure when price is negative."""
    payload = {"name": "Discount Coupon", "price": -10.50}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_product_missing_required_price(client: TestClient) -> None:
    """Test validation failure when required price field is omitted."""
    payload = {"name": "Headphones"}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_product_invalid_data_types(client: TestClient) -> None:
    """Test validation failure when field types are invalid."""
    payload = {"name": "Monitor", "price": "not-a-number"}
    response = client.post("/products", json=payload)
    assert response.status_code == 422


# ============================================================================
# Product Retrieval (GET /products and GET /products/{id})
# ============================================================================


def test_get_all_products_empty(client: TestClient) -> None:
    """Test retrieving products when store is empty returns empty list."""
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_products_populated(client: TestClient) -> None:
    """Test retrieving all products when store contains multiple items."""
    client.post("/products", json={"name": "Item A", "price": 15.00})
    client.post("/products", json={"name": "Item B", "price": 25.50})

    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item A"
    assert data[1]["name"] == "Item B"


def test_get_product_by_id_success(client: TestClient) -> None:
    """Test retrieving a single product by its existing ID."""
    created = client.post(
        "/products",
        json={"name": "Desk Lamp", "description": "LED lamp", "price": 45.00},
    ).json()

    response = client.get(f"/products/{created['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["name"] == "Desk Lamp"
    assert data["price"] == 45.00


def test_get_product_by_id_not_found(client: TestClient) -> None:
    """Test retrieving a non-existent product returns 404."""
    response = client.get("/products/9999")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


# ============================================================================
# Product Update (PUT /products/{id})
# ============================================================================


def test_update_product_success(client: TestClient) -> None:
    """Test updating all fields of an existing product."""
    created = client.post(
        "/products",
        json={"name": "Old Name", "description": "Old desc", "price": 20.00},
    ).json()

    update_payload = {
        "name": "New Name",
        "description": "Updated desc",
        "price": 35.00,
        "in_stock": False,
    }
    response = client.put(f"/products/{created['id']}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["name"] == "New Name"
    assert data["description"] == "Updated desc"
    assert data["price"] == 35.00
    assert data["in_stock"] is False


def test_update_product_partial(client: TestClient) -> None:
    """Test updating only a subset of fields preserves unchanged values."""
    created = client.post(
        "/products",
        json={"name": "Coffee Mug", "description": "Ceramic", "price": 12.00},
    ).json()

    response = client.put(f"/products/{created['id']}", json={"price": 15.50})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Coffee Mug"
    assert data["description"] == "Ceramic"
    assert data["price"] == 15.50


def test_update_product_not_found(client: TestClient) -> None:
    """Test updating a non-existent product returns 404."""
    response = client.put("/products/9999", json={"name": "Ghost Item"})
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_update_product_invalid_price(client: TestClient) -> None:
    """Test updating with negative price returns 422."""
    created = client.post(
        "/products",
        json={"name": "Notebook", "price": 5.00},
    ).json()

    response = client.put(f"/products/{created['id']}", json={"price": -1.00})
    assert response.status_code == 422


def test_update_product_empty_name(client: TestClient) -> None:
    """Test updating with empty name returns 422."""
    created = client.post(
        "/products",
        json={"name": "Notebook", "price": 5.00},
    ).json()

    response = client.put(f"/products/{created['id']}", json={"name": "  "})
    assert response.status_code == 422


# ============================================================================
# Product Deletion (DELETE /products/{id})
# ============================================================================


def test_delete_product_success(client: TestClient) -> None:
    """Test deleting an existing product returns 204 No Content."""
    created = client.post(
        "/products",
        json={"name": "Item to Delete", "price": 10.00},
    ).json()

    delete_response = client.delete(f"/products/{created['id']}")
    assert delete_response.status_code == 204

    # Verify item no longer exists
    get_response = client.get(f"/products/{created['id']}")
    assert get_response.status_code == 404


def test_delete_product_not_found(client: TestClient) -> None:
    """Test deleting a non-existent product returns 404."""
    response = client.delete("/products/9999")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
