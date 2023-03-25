from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

user_details =  { # test user
        "id": 1,
        "username": "timosky",
        "email": "timosky@gmail.com",
        "api_key": "45204d1f38324b4ea349218c31a6cc71"
    }

def test_expert_endpoint():
    # test correct response
    api_key = user_details["api_key"]
    response = client.get(f"/experts?tag=python&api_key={api_key}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 9
    assert "reps" in data[0]
    assert "user_id" in data[0]
    assert "number_of_answers" in data[0]


    # test wrong post request
    response = client.post(f"/experts?tag=python&api_key={api_key}")
    assert response.status_code == 405, response.text