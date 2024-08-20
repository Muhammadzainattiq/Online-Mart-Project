from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select
from app.main import app
from app.db.db_connection import get_session
from app.models.user_models import User, PaymentDetails
from app.kafka.producer import KAFKA_PRODUCER
# Create the test engine
DATABASE_TEST_URL = "postgresql://zain:password@test_db:5432/testdb"
test_engine = create_engine(DATABASE_TEST_URL, echo=True)

@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture(name="session")
def session_fixture():
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="mock_producer")
def mock_producer_fixture():
    return AsyncMock()

@pytest.fixture(name="client")
def client_fixture(session: Session, setup_db, mock_producer):
    def get_test_db():
        yield session
    
    app.dependency_overrides[get_session] = get_test_db
    app.dependency_overrides[KAFKA_PRODUCER] = lambda: mock_producer
    return TestClient(app)

# def test_add_user_payment_details(client: TestClient, session: Session, mock_producer):
#     # Step 1: Create a user
#     user_data = {
#         "user_email": "user2@example.com",
#         "user_password": "string",
#         "user_name": "User Two",
#         "phone_number": "1234567890",
#         "user_address": "456 Main St"
#     }
#     response = client.post("/user_auth/signup_user", json=user_data)
#     assert response.status_code == 200

#     # Commit the session to save the user in the database
#     session.commit()

#     # Step 2: Retrieve the user
#     statement = select(User).where(User.user_email == "user2@example.com")
#     user_in_db = session.exec(statement).first()
#     assert user_in_db is not None, "User was not created successfully"
#     user_id = user_in_db.user_id

#     # Step 3: Add payment details with a new client request
#     payment_details = {
#         "card_number": "9876543210123456",
#         "card_expiry": "11/26",
#         "card_cvc": "321"
#     }
    
#     response = client.post(f"/user/add_user_payment_details?user_id={user_id}", json=payment_details)
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["card_number"] == payment_details["card_number"]
# #     assert response_data["user_id"] == user_id




# def test_get_payment_details(client: TestClient, session: Session):
#     # Step 1: Create a user
#     user_data = {
#         "user_email": "user3@example.com",  # Use a unique email to avoid conflicts
#         "user_password": "string",
#         "user_name": "User Three",
#         "phone_number": "1234567890",
#         "user_address": "456 Main St"
#     }
#     response = client.post("/user_auth/signup_user", json=user_data)
#     assert response.status_code == 200

#     # Commit the session to save the user in the database
#     session.commit()
    
#     # Step 2: Retrieve the user
#     statement = select(User).where(User.user_email == "user3@example.com")  # Ensure correct email
#     user_in_db = session.exec(statement).first()
#     assert user_in_db is not None, "User was not created successfully"
#     user_id = user_in_db.user_id

#     # Ensure the session is fully flushed
#     session.refresh(user_in_db)

#     # Step 3: Add payment details with a new client request
#     payment_details = {
#         "card_number": "9876543210123456",
#         "card_expiry": "11/26",
#         "card_cvc": "321"
#     }
#     response = client.post(
#         f"/user/add_user_payment_details?user_id={user_id}",
#         json=payment_details
#     )

#     # Debugging Information
#     print(f"Response status code: {response.status_code}")
#     print(f"Response content: {response.content}")

#     # Final assertion to ensure the request was successful
#     assert response.status_code == 200



def test_get_user_by_id(client: TestClient, session: Session):
    # Create a user first
    user = {
        "user_email": "user1@example.com",
        "user_password": "string",
        "user_name": "User Three",
        "phone_number": "9876543210",  # Phone number as string
        "user_address": "789 Broadway"
    }
    response = client.post("/user_auth/signup_user", json=user)
    assert response.status_code == 200

    # Retrieve the user_id
    statement = select(User).where(User.user_email == "user1@example.com")
    user_in_db = session.exec(statement).first()
    assert user_in_db is not None, "User was not created successfully"
    user_id = user_in_db.user_id

    # Test getting user by ID
    response = client.get(f"/user/get_user_by_id/{user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user_id"] == user_id
    assert response_data["user_email"] == user["user_email"]
    assert response_data["user_name"] == user["user_name"]



def test_get_user_by_email(client: TestClient, session: Session):
    # Create a user first
    user = {
        "user_email": "user4@example.com",
        "user_password": "string",
        "user_name": "User Four",
        "phone_number": "1231231234",  # Phone number as string
        "user_address": "101 First St"
    }
    response = client.post("/user_auth/signup_user", json=user)
    assert response.status_code == 200

    # Test getting user by email
    response = client.get(f"/user/get_user_by_email/{user['user_email']}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user_email"] == user["user_email"]
    assert response_data["user_name"] == user["user_name"]



def test_get_all_users(client: TestClient, session: Session):
    # Create multiple users
    users = [
        {
            "user_email": "user5@example.com",
            "user_password": "string",
            "user_name": "User Five",
            "phone_number": "1112223333",  # Phone number as string
            "user_address": "202 Second St"
        },
        {
            "user_email": "user6@example.com",
            "user_password": "string",
            "user_name": "User Six",
            "phone_number": "4445556666",  # Phone number as string
            "user_address": "303 Third St"
        }
    ]
    for user in users:
        response = client.post("/user_auth/signup_user", json=user)
        assert response.status_code == 200

    # Test getting all users
    response = client.get("/user/get_all_users")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= len(users)  # Ensure the users were created



def test_delete_user(client: TestClient, session: Session):
    # Create a user first
    user = {
        "user_email": "user7@example.com",
        "user_password": "string",
        "user_name": "User Seven",
        "phone_number": "7778889999",  # Phone number as string
        "user_address": "404 Fourth St"
    }
    response = client.post("/user_auth/signup_user", json=user)
    assert response.status_code == 200

    # Retrieve the user_id
    statement = select(User).where(User.user_email == "user7@example.com")
    user_in_db = session.exec(statement).first()
    assert user_in_db is not None, "User was not created successfully"
    user_id = user_in_db.user_id

    # Test deleting the user
    response = client.delete(f"/user/delete_user/{user_id}")
    assert response.status_code == 200

    # Verify the user was deleted
    user_in_db = session.exec(statement).first()
    assert user_in_db is None, "User was not deleted successfully"



def test_update_user(client: TestClient, session: Session):
    # Create a user first
    user = {
        "user_email": "user8@example.com",
        "user_password": "string",
        "user_name": "User Eight",
        "phone_number": "8889990000",  # Phone number as string
        "user_address": "505 Fifth St"
    }
    response = client.post("/user_auth/signup_user", json=user)
    assert response.status_code == 200

    # Retrieve the user_id
    statement = select(User).where(User.user_email == "user8@example.com")
    user_in_db = session.exec(statement).first()
    assert user_in_db is not None, "User was not created successfully"
    user_id = user_in_db.user_id

    # Test updating the user
    updated_user = {
        "user_name": "Updated User Eight",
        "phone_number": "1234567890"  # Updated phone number as string
    }
    response = client.put(f"/user/update_user/{user_id}", json=updated_user)
    assert response.status_code == 200

    # Verify the user was updated
    user_in_db = session.exec(statement).first()
    assert user_in_db.user_name == updated_user["user_name"]
    assert user_in_db.phone_number == updated_user["phone_number"]

