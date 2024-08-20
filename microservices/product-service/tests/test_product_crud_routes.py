import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select
from app.main import app  # Adjust the import based on your FastAPI app location
from app.db.db_connection import get_session
from app.models.product_models import Product, Category, Size, Color
import warnings

# Override the DATABASE_URL to use the test database
DATABASE_TEST_URL = "postgresql://zain:password@test_db:5432/testdb"

# Create engine for the test database
test_engine = create_engine(DATABASE_TEST_URL, echo=True)

# Setup the test database engine
@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(test_engine)  # Create tables
    yield
    SQLModel.metadata.drop_all(test_engine)  # Clean up after tests

# Fixture to provide a session that uses the test database
@pytest.fixture(name="session")
def session_fixture():
    with Session(test_engine) as session:
        yield session

# Override the dependency to use the test session
@pytest.fixture(name="client")
def client_fixture(session: Session, setup_db, mock_producer):  # Include setup_db here
    def get_test_db():
        yield session

    app.dependency_overrides[get_session] = get_test_db

    # Override the Kafka producer
    # app.dependency_overrides["KAFKA_PRODUCER"] = lambda: mock_producer
    
    return TestClient(app)

@pytest.fixture(name="mock_producer")
def mock_producer_fixture():
    mock_producer = AsyncMock()
    return mock_producer

# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="passlib.utils")

  # Adjust the import based on your FastAPI app location

def test_create_product_route_with_product_name_missing(client: TestClient):
    # Define the test data without product_name
    product_data = {
        "product_description": "A test product",
        "product_price": 99.99,
        "product_image_url": "http://example.com/test_product.png",
        "product_category_ids": [],
        "colors": [],
        "sizes": []
    }

    # Send a POST request to the /add_product route
    response = client.post("/product/add_product", json=product_data)

    # Verify the response status code
    assert response.status_code == 422  # 422 Unprocessable Entity

    # Verify the response error message
    response_data = response.json()
    assert "product_name" in response_data["detail"][0]["loc"]
    assert "field required" in response_data["detail"][0]["msg"]

# def test_create_product(client: TestClient, session: Session):
#     # Step 1: Create necessary categories, colors, and sizes
#     category = Category(category_name="Electronics", category_description="Electronic Items")
#     session.add(category)
#     session.commit()
#     session.refresh(category)
    
#     color = Color(color_name="Red")
#     session.add(color)
#     session.commit()
#     session.refresh(color)
    
#     size = Size(size_name="Large")
#     session.add(size)
#     session.commit()
#     session.refresh(size)# Unit test for the /add_product route
    
#     # Step 2: Create a product with the created categories, colors, and sizes
#     product_data = {
#         "product_name": "Smartphone",
#         "product_description": "A smartphone with various features.",
#         "product_price": 999.99,
#         "product_image_url": "http://example.com/image.png",
#         "product_category_ids": [category.category_id],
#         "colors": [{"color_name": "Red"}],
#         "sizes": [{"size_name": "Large"}]
#     }
#     response = client.post("/product/add_product", json=product_data)
#     assert response.status_code == 200

#     # Verify the product was created
#     statement = select(Product).where(Product.product_name == "Smartphone")
#     product_in_db = session.exec(statement).first()
#     assert product_in_db is not None, "Product was not created successfully"
#     assert product_in_db.product_name == "Smartphone"

#     # Verify the product's categories, colors, and sizes were added
#     product_categories = session.exec(select(ProductCategory).where(ProductCategory.product_id == product_in_db.product_id)).all()
#     assert len(product_categories) == 1

#     product_colors = session.exec(select(ProductColor).where(ProductColor.product_id == product_in_db.product_id)).all()
#     assert len(product_colors) == 1

#     product_sizes = session.exec(select(ProductSize).where(ProductSize.product_id == product_in_db.product_id)).all()
#     assert len(product_sizes) == 1


# def test_read_products_by_name(client: TestClient, session: Session):
#     # Fetch products by name
#     response = client.get("/product/read_products_by_name/Smartphone")
#     assert response.status_code == 200

#     products = response.json()
#     assert len(products) > 0
#     assert products[0]["product_name"] == "Smartphone"


# def test_read_products_by_category(client: TestClient, session: Session):
#     # Fetch products by category
#     response = client.get("/product/read_products_by_category/Electronics")
#     assert response.status_code == 200

#     products = response.json()
#     assert len(products) > 0
#     assert "Electronics" in [category['category_name'] for category in products[0]["categories"]]



# # Test Read Product by ID
# def test_read_product_by_id(client: TestClient, session: Session):
#     # Create a product
#     product = Product(product_name="Laptop", product_description="Gaming Laptop", product_price=1500.00, product_image_url="http://example.com/laptop.png")
#     session.add(product)
#     session.commit()
#     session.refresh(product)

#     # Fetch the product by ID
#     response = client.get(f"/product/read_product_by_id/{product.product_id}")
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["product_name"] == "Laptop"






# # Test Read All Products
# def test_read_all_products(client: TestClient, session: Session):
#     # Fetch all products
#     response = client.get("/product/read_all_products")
#     assert response.status_code == 200
#     response_data = response.json()
#     assert len(response_data) > 0

# # Test Read Products with Pagination
# def test_read_products_with_pagination(client: TestClient, session: Session):
#     # Fetch products with pagination
#     response = client.get("/product/read_all_products_with_pagination?offset=0&limit=5")
#     assert response.status_code == 200
#     response_data = response.json()
#     assert len(response_data) > 0

# # Test Update Product by ID
# def test_update_product_by_id(client: TestClient, session: Session):
#     # Create a product to update
#     product = Product(product_name="Tablet", product_description="Android Tablet", product_price=299.99, product_image_url="http://example.com/tablet.png")
#     session.add(product)
#     session.commit()
#     session.refresh(product)

#     # Update the product
#     updated_data = {
#         "product_name": "Updated Tablet",
#         "product_price": 279.99
#     }
#     response = client.put(f"/product/update_product/{product.product_id}", json=updated_data)
#     assert response.status_code == 200

#     # Verify the product update
#     updated_product = session.get(Product, product.product_id)
#     assert updated_product.product_name == "Updated Tablet"
#     assert updated_product.product_price == 279.99

# # Test Delete Product by ID
# def test_delete_product_by_id(client: TestClient, session: Session):
#     # Create a product to delete
#     product = Product(product_name="Smartwatch", product_description="Wearable Smartwatch", product_price=199.99, product_image_url="http://example.com/smartwatch.png")
#     session.add(product)
#     session.commit()
#     session.refresh(product)

#     # Delete the product
#     response = client.delete(f"/product/delete_product/{product.product_id}")
#     assert response.status_code == 200

#     # Verify the product deletion
#     deleted_product = session.get(Product, product.product_id)
#     assert deleted_product is None
