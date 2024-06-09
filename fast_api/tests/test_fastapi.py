# fast_api/tests/test_fastapi.py
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from pymongo import MongoClient
from inputapi import app  # Adjust this import if your FastAPI app is in a different file

# Create a test client using the FastAPI application
client = TestClient(app)

# Define a fixture for the MongoDB client
@pytest.fixture(scope="module")
def test_db():
    client = MongoClient("mongodb://root:maor@localhost:27017/mydb?authSource=admin")
    db = client["mydb"]
    yield db
    client.drop_database("mydb")

def test_get_customers(test_db):
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == {"table": []}

def test_create_customer(test_db):
    customer = {"name": "John Doe", "mail": "john@example.com", "phone": "1234567890"}
    response = client.post("/input", json=customer)
    assert response.status_code == 200
    assert response.json() == {"message": "Customer created successfully."}

    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == {"table": [customer]}

def test_create_product(test_db):
    products = [
        {"id": "1", "name": "Product A", "provider": "Provider X"},
        {"id": "2", "name": "Product B", "provider": "Provider Y"}
    ]
    response = client.post("/input_product", json=products)
    assert response.status_code == 200
    assert response.json() == {"message": "Products created successfully."}

    response = client.get("/product")
    assert response.status_code == 200
    assert response.json() == {"table": products}
