from fastapi.testclient import TestClient
from app.routes.product_crud_routes import product_router
from app.models.product_models import ProductCreate

# Initialize the TestClient with the FastAPI app
client = TestClient(product_router)

def test_create_product_missing_fields():
    response = client.post("/product/add_product", json={})
    assert response.status_code == 400

def test_create_product_with_empty_name():
    response = client.post(
        "/product/add_product",
        json={"product_name": "", "product_description": "Test Product", "product_price": 10.0, "product_category_ids": [1]},
    )
    assert response.status_code == 400

def test_create_product_with_invalid_image_url():
    invalid_product_data = {
        "product_name": "Test Product",
        "product_description": "This is a test product",
        "product_price": 100.00,
        "product_category_ids": [1],
        "product_image_url": "invalid_url"
    }
    response = client.post("/product/add_product", json=invalid_product_data)
    assert response.status_code == 400

def test_add_product_with_decimal_price():
    product_data = {
        "product_name": "Test Product",
        "product_description": "A product with a decimal price",
        "product_price": 10.99,
        "product_category_ids": [1]
    }
    response = client.post("/product/add_product", json=product_data)
    assert response.status_code == 200
    assert response.json()["product_name"] == product_data["product_name"]

def test_add_product_with_special_characters():
    product_name = "Special Product@123"
    product_category_ids = [1]
    response = client.post(
        "/product/add_product",
        json={"product_name": product_name, "product_category_ids": product_category_ids},
    )
    assert response.status_code == 200
    assert response.json()["product_name"] == product_name

def test_create_product_with_unique_name():
    product1 = {
        "product_name": "Test Product 1",
        "product_description": "Test Description 1",
        "product_price": 100.0,
        "product_category_ids": [1]
    }
    response1 = client.post("/product/add_product", json=product1)
    assert response1.status_code == 200

    product2 = {
        "product_name": "Test Product 1",
        "product_description": "Test Description 2",
        "product_price": 200.0,
        "product_category_ids": [1]
    }
    response2 = client.post("/product/add_product", json=product2)
    assert response2.status_code == 400
    assert "Product name must be unique" in response2.json()["detail"]

def test_concurrent_add_products():
    products_data = [
        {"product_name": f"Product{i}", "product_description": "Test product", "product_price": 10.0, "product_category_ids": [1]}
        for i in range(10)
    ]
    responses = [
        client.post("/product/add_product", json=product_data)
        for product_data in products_data
    ]
    for response in responses:
        assert response.status_code == 200

def test_create_product_returns_201_status_code():
    response = client.post(
        "/product/add_product",
        json={"product_name": "Test Product", "product_description": "Test Description", "product_price": 9.99, "product_category_ids": [1]},
    )
    assert response.status_code == 201

def test_create_product_with_zero_quantity():
    product_data = {
        "product_name": "Test Product",
        "product_description": "Test Description",
        "product_price": 100.0,
        "product_category_ids": [1],
        "quantity": 0
    }
    response = client.post("/product/add_product", json=product_data)
    assert response.status_code == 400

def test_create_product_with_negative_price():
    negative_price_product = ProductCreate(
        product_name="Test Product", product_price=-10.0, product_category_ids=[1]
    )
    response = client.post("/product/add_product", json=negative_price_product.dict())
    assert response.status_code == 400
