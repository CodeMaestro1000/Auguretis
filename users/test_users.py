import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db.database import Base
from db.session import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine) # drop all tables first before testing

"""The fixtures ensures that the database is created and dropped before and after running all tests"""
@pytest.fixture(scope="class")
def session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="class")
def client(session):

    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


# temp fix to update api_key in class



@pytest.mark.usefixtures("client")
class TestUsers:
    user_email = "testuser@example.com"
    user_password = "testpassword"
    username = "test_user"
    updated_username = "test_user_updated"
    secret_key = 'test-secret-key'

    def login(self, client, username = None, password = None):
        if not username:
            username = self.username
        if not password:
            password = self.user_password
        files = {
            'username': (None, username),
            'password': (None, password),
        }
        response = client.post("/login", files=files)
        return response.json()["access_token"]

    def test_create_user(self, client):
        # create user endpoint
        response = client.post(
            "users/new-superuser",
            json={"email": self.user_email, "password": self.user_password, "username": self.username},
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == self.user_email
        assert data["username"] == self.username
        assert "api_key" in data
        assert "password" not in data
    
    def test_list_user(self, client):
        # list all users endpoint
        token = self.login(client)
        head = {'Authorization': 'Bearer ' + token}
        response = client.get("/users/all/", headers=head)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 1
        assert data[0]['email'] == self.user_email

    def test_get_users(self, client):
        # get user end point
        token = self.login(client)
        head = {'Authorization': 'Bearer ' + token}
        response = client.get("/users/1/", headers=head)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["username"] == self.username
        api_key = data["api_key"]

        # get user by api_key
        response = client.get(f"/users?api_key={api_key}", headers=head)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["username"] == self.username
    
    def test_duplicate_exception(self, client):
        # test duplicate email exception
        response = client.post(
            "users/new/",
            json={"email": self.user_email, "password": self.user_password, "username": self.username},
        )
        assert response.status_code == 400, response.text
        data = response.json()
        assert data['detail'] == 'User with email already exists'

        # test duplicate username exception
        response = client.post(
            "users/new/",
            json={"email":'anotheremail@test.com', "password": self.user_password, "username": self.username},
        )
        assert response.status_code == 400, response.text
        data = response.json()
        assert data['detail'] == 'User with username already exists'

    def test_not_found_exception(self, client):
        # test not found exception
        token = self.login(client)
        head = {'Authorization': 'Bearer ' + token}
        response = client.get("/users/100/", headers=head)
        assert response.status_code == 400, response.text
        data = response.json()
        assert data["detail"] == "User does not exist"

    def test_update_user(self, client):
        # update endpoint
        token = self.login(client)
        head = {'Authorization': 'Bearer ' + token}
        response = client.post(
            "users/user-update/",
            json={"new_username": self.updated_username, "username": self.username},
            headers = head
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["username"] == self.updated_username

    def test_delete_user(self, client):
        # delete endpoint
        token = self.login(client, self.updated_username)
        head = {'Authorization': 'Bearer ' + token}
        response = client.post(
            f"users/delete/{self.updated_username}",
            headers = head
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["id"] == 1
        assert data["username"] == self.updated_username
        assert data["email"] == self.user_email