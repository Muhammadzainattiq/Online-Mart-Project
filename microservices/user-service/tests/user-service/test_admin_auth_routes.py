#The commented out tests are related to kong. 


import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select
from app.main import app  # Adjust the import based on your FastAPI app location
from app.db.db_connection import get_session
import os
from app.models.user_models import User, PaymentDetails
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
def client_fixture(session: Session, setup_db):  # Include setup_db here
    def get_test_db():
        yield session
    
    app.dependency_overrides[get_session] = get_test_db
    return TestClient(app)


# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="passlib.utils")

# def test_signup_admin_success(client: TestClient, session: Session):
#     # Step 1: Create a new admin
#     admin_data = {
#         "admin_email": "new_admin@example.com",
#         "admin_password": "securepassword",
#         "admin_name": "New Admin",
#         "phone_number": "1112223333",
#         "admin_address": "123 Admin St"
#     }

#     # Step 2: Send the signup request
#     response = client.post("/admin_auth/signup_admin", json=admin_data)
    
#     # Step 3: Verify the response
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["message"] == "You are successfully registered"

#     # Step 4: Verify the admin is in the database
#     statement = select(Admin).where(Admin.admin_email == admin_data["admin_email"])
#     admin_in_db = session.exec(statement).first()
#     assert admin_in_db is not None, "Admin was not created successfully"
#     assert admin_in_db.admin_email == admin_data["admin_email"]


# def test_signup_admin_already_exists(client: TestClient, session: Session):
#     # Step 1: Create an admin first to simulate an existing admin
#     existing_admin_data = {
#         "admin_email": "existing_admin@example.com",
#         "admin_password": "securepassword",
#         "admin_name": "Existing Admin",
#         "phone_number": "4445556666",
#         "admin_address": "456 Existing St"
#     }
#     client.post("/admin_auth/signup_admin", json=existing_admin_data)
#     session.commit()

#     # Step 2: Try to sign up with the same email
#     response = client.post("/admin_auth/signup_admin", json=existing_admin_data)
    
#     # Step 3: Verify the response
#     assert response.status_code == 409
#     response_data = response.json()
#     assert response_data["detail"] == "Admin Already Exists. Please try signing in."


from unittest.mock import patch

# @patch("app.handlers.admin_auth.create_jwt_credentials", return_value={"key": "mock-key", "secret": "mock-secret"})
# @patch("app.handlers.admin_auth.get_kong_jwt_token", return_value="mock-jwt-token")
# def test_login_admin_success(mock_create_jwt_credentials, mock_get_kong_jwt_token, client: TestClient, session: Session):
#     # Step 1: Create an admin first to log in with
#     admin_data = {
#         "admin_email": "login_admin@example.com",
#         "admin_password": "securepassword",
#         "admin_name": "Login Admin",
#         "phone_number": "7778889999",
#         "admin_address": "789 Admin St"
#     }
#     client.post("/admin_auth/signup_admin", json=admin_data)
#     session.commit()

#     # Step 2: Log in with the correct credentials
#     login_data = {
#         "admin_email": "login_admin@example.com",
#         "admin_password": "securepassword"
#     }
#     response = client.post("/admin_auth/login_admin", json=login_data)
    
#     # Step 3: Verify the response
#     assert response.status_code == 200
#     response_data = response.json()
#     assert "token" in response_data  # Check if the token is returned


# @patch("app.handlers.admin_auth.create_jwt_credentials", return_value={"key": "mock-key", "secret": "mock-secret"})
# @patch("app.handlers.admin_auth.get_kong_jwt_token", return_value="mock-jwt-token")
# def test_login_admin_invalid_password(mock_create_jwt_credentials, mock_get_kong_jwt_token, client: TestClient, session: Session):
#     # Step 1: Create an admin first to log in with
#     admin_data = {
#         "admin_email": "login_invalid_admin@example.com",
#         "admin_password": "securepassword",
#         "admin_name": "Login Invalid Admin",
#         "phone_number": "1112223333",
#         "admin_address": "123 Invalid St"
#     }
#     client.post("/admin_auth/signup_admin", json=admin_data)
#     session.commit()

#     # Step 2: Attempt to log in with an incorrect password
#     login_data = {
#         "admin_email": "login_invalid_admin@example.com",
#         "admin_password": "wrongpassword"
#     }
#     response = client.post("/admin_auth/login_admin", json=login_data)
    
#     # Step 3: Verify the response
#     assert response.status_code == 401
#     response_data = response.json()
#     assert response_data["detail"] == "Invalid password"


def test_login_admin_not_found(client: TestClient, session: Session):
    # Step 1: Attempt to log in with a non-existent email
    login_data = {
        "admin_email": "non_existent_admin@example.com",
        "admin_password": "somepassword"
    }
    response = client.post("/admin_auth/login_admin", json=login_data)
    
    # Step 2: Verify the response
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Admin not found"


# @patch("app.handlers.admin_auth.get_kong_jwt_token", return_value="mock-jwt-token")
# def test_get_admin_success(mock_get_kong_jwt_token, client: TestClient, session: Session):
#     # Step 1: Create an admin first to log in and get the token
#     admin_data = {
#         "admin_email": "get_admin@example.com",
#         "admin_password": "securepassword",
#         "admin_name": "Get Admin",
#         "phone_number": "3334445555",
#         "admin_address": "101 Admin St"
#     }
#     client.post("/admin_auth/signup_admin", json=admin_data)
#     session.commit()

#     # Step 2: Log in to get the token
#     login_data = {
#         "admin_email": "get_admin@example.com",
#         "admin_password": "securepassword"
#     }
#     response = client.post("/admin_auth/login_admin", json=login_data)
#     assert response.status_code == 200
#     token = response.json()["token"]

#     # Step 3: Use the token to get the admin details
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/admin_auth/get_admin", headers=headers)
    
#     # Step 4: Verify the response
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["admin_email"] == admin_data["admin_email"]
#     assert response_data["admin_name"] == admin_data["admin_name"]


def test_get_admin_invalid_token(client: TestClient):
    # Step 1: Use an invalid token
    invalid_token = "invalidtoken"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get("/admin_auth/get_admin", headers=headers)
    
    # Step 2: Verify the response
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Token not found"


