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


def test_signup_user_success(client: TestClient, session: Session):
    # Step 1: Create a new user
    user_data = {
        "user_email": "new_user@example.com",
        "user_password": "securepassword",
        "user_name": "New User",
        "phone_number": "1112223333",  # Phone number as string
        "user_address": "123 New St"
    }

    # Step 2: Send the signup request
    response = client.post("/user_auth/signup_user/", json=user_data)
    
    # Step 3: Verify the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "You are successfully registered"

    # Step 4: Verify the user is in the database
    statement = select(User).where(User.user_email == user_data["user_email"])
    user_in_db = session.exec(statement).first()
    assert user_in_db is not None, "User was not created successfully"
    assert user_in_db.user_email == user_data["user_email"]


def test_signup_user_already_exists(client: TestClient, session: Session):
    # Step 1: Create a user first to simulate an existing user
    existing_user_data = {
        "user_email": "existing_user@example.com",
        "user_password": "securepassword",
        "user_name": "Existing User",
        "phone_number": "4445556666",
        "user_address": "456 Existing St"
    }
    client.post("/user_auth/signup_user/", json=existing_user_data)
    session.commit()

    # Step 2: Try to sign up with the same email
    response = client.post("/user_auth/signup_user/", json=existing_user_data)
    
    # Step 3: Verify the response
    assert response.status_code == 409
    response_data = response.json()
    assert response_data["detail"] == "User Already Exists. Please try signing in."


# def test_login_user_success(client: TestClient, session: Session):
#     # Step 1: Create a user first to log in with
#     user_data = {
#         "user_email": "login_user@example.com",
#         "user_password": "securepassword",
#         "user_name": "Login User",
#         "phone_number": "7778889999",
#         "user_address": "789 Login St"
#     }
#     client.post("/user_auth/signup_user/", json=user_data)
#     session.commit()

#     # Step 2: Log in with the correct credentials
#     login_data = {
#         "user_email": "login_user@example.com",
#         "user_password": "securepassword"
#     }
#     response = client.post("/user_auth/login_user/", json=login_data)
    
#     # Step 3: Verify the response
#     assert response.status_code == 200
#     response_data = response.json()
#     assert "token" in response_data  # Check if the token is returned


# def test_login_user_invalid_password(client: TestClient, session: Session):
#     # Step 1: Create a user first to log in with
#     user_data = {
#         "user_email": "login_invalid_user@example.com",
#         "user_password": "securepassword",
#         "user_name": "Login Invalid User",
#         "phone_number": "1112223333",
#         "user_address": "123 Invalid St"
#     }
#     client.post("/user_auth/signup_user/", json=user_data)
#     session.commit()

#     # Step 2: Attempt to log in with an incorrect password
#     login_data = {
#         "user_email": "login_invalid_user@example.com",
#         "user_password": "wrongpassword"
#     }
#     response = client.post("/user_auth/login_user/", json=login_data)
    
#     # Step 3: Verify the response
#     assert response.status_code == 401
#     response_data = response.json()
#     assert response_data["detail"] == "Invalid password"


def test_login_user_not_found(client: TestClient, session: Session):
    # Step 1: Attempt to log in with a non-existent email
    login_data = {
        "user_email": "non_existent_user@example.com",
        "user_password": "somepassword"
    }
    response = client.post("/user_auth/login_user/", json=login_data)
    
    # Step 2: Verify the response
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "User not found"

#related to kong that why commented

# def test_get_user_success(client: TestClient, session: Session):
#     # Step 1: Create a user first to log in and get the token
#     user_data = {
#         "user_email": "get_user@example.com",
#         "user_password": "securepassword",
#         "user_name": "Get User",
#         "phone_number": "3334445555",
#         "user_address": "101 GetUser St"
#     }
#     client.post("/user_auth/signup_user/", json=user_data)
#     session.commit()

#     # Step 2: Log in to get the token
#     login_data = {
#         "user_email": "get_user@example.com",
#         "user_password": "securepassword"
#     }
#     response = client.post("/user_auth/login_user/", json=login_data)
#     assert response.status_code == 200
#     token = response.json()["token"]

#     # Step 3: Use the token to get the user details
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/user_auth/get_user/", headers=headers)
    
#     # Step 4: Verify the response
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["user_email"] == user_data["user_email"]
#     assert response_data["user_name"] == user_data["user_name"]


def test_get_user_invalid_token(client: TestClient):
    # Step 1: Use an invalid token
    invalid_token = "invalidtoken"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.get("/user_auth/get_user/", headers=headers)
    
    # Step 2: Verify the response
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Token not found"
