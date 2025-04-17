import pytest
from fastapi.testclient import TestClient
from sqlalchemy import engine
from create_db import Base, OrderProduct, Plant, PlantMaterial, PlantProduct, Product, Material, ProductMaterial, StorageProduct, StorageMaterial, Order
from fastapi5 import app,SessionLocal,get_db


# Testing
# Create a TestClient for the FastAPI app
client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    # Create the database schema
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database schema after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def override_get_db(test_db):
    # Override the get_db dependency to use the test database
    def get_db_override():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db_override
    yield
    # del app.dependency_overrides[get_db]

# Plant Tests
def test_create_plant():
    response = client.post("/plants/", json={"name": "Test Plant", "location": "Test Location", "capacity": 1000})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Plant"

def test_read_plant():
    plant_data = {"name": "Read Plant", "location": "Read Location", "capacity": 500}
    create_response = client.post("/plants/", json=plant_data)
    plant_id = create_response.json()["id"]
    response = client.get(f"/plants/{plant_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Read Plant"