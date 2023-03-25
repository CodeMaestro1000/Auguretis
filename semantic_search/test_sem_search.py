from fastapi.testclient import TestClient
import requests
from main import app

client = TestClient(app)

user_details =  { # test user
        "id": 1,
        "username": "timosky",
        "email": "timosky@gmail.com",
        "api_key": "45204d1f38324b4ea349218c31a6cc71"
    }

def test_endpoint():
    api_key = user_details['api_key']
    query = {"query": "Dependency Injection", "api_key": api_key}
    response = client.post("/search", json=query)
    assert response.status_code == 200, response.text
    assert "results" in response.json()

    # test wrong post request
    response = client.get(f"/search")
    assert response.status_code == 405, response.text