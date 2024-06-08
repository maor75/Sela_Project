import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pymongo import MongoClient
import mongomock
from inputapi import app, MONGO_DB_NAME

# Override the MongoDB client with a mock for testing
mock_client = mongomock.MongoClient()
db = mock_client[MONGO_DB_NAME]
app.dependency_overrides[MongoClient] = lambda: mock_client

# Create a TestClient instance for synchronous testing
client = TestClient(app)

# Use httpx.AsyncClient for asynchronous tests
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def test_db():
    """Fixture to setup and teardown the mock database."""
    db.customers.drop()
    db.products.drop()

    # Insert sample data if needed
    db.customers.insert_many([
        {"name": "John Doe", "mail": "john@example.com", "phone": "1234567890"},
        {"name": "Jane Doe", "mail": "jane@example.com", "phone": "0987654321"}
    ])
    db.products.insert_many([
        {"id": "1", "name": "Product A", "provider": "Provider 1"},
        {"id": "2", "name": "Product B", "provider": "Provider 2"}
    ])

    return db

# Test GET /customers
def test_get_customers(test_db):
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == {
        "table": [
            {"name": "John Doe", "mail": "john@example.com", "phone": "1234567890"},
            {"name": "Jane Doe", "mail": "jane@example.com", "phone": "0987654321"}
        ]
    }

# Test GET /product
def test_get_products(test_db):
    response = client.get("/product")
    assert response.status_code == 200
    assert response.json() == {
        "table": [
            {"id": "1", "name": "Product A", "provider": "Provider 1"},
            {"id": "2", "name": "Product B", "provider": "Provider 2"}
        ]
    }

# Test POST /input
def test_create_customer(test_db):
    response = client.post("/input", json={
        "name": "Alice",
        "mail": "alice@example.com",
        "phone": "1234567890"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}
    customer = db.customers.find_one({"mail": "alice@example.com"})
    assert customer is not None

# Test POST /input_product
def test_create_product(test_db):
    response = client.post("/input_product", json=[
        {"id": "3", "name": "Product C", "provider": "Provider 3"}
    ])
    assert response.status_code == 200
    assert response.json() == {"message": "Products created successfully."}
    product = db.products.find_one({"id": "3"})
    assert product is not None
    assert product["name"] == "Product C"
