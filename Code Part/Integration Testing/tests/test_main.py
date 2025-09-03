from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Payload : When you are sending data to the API
# Response : When you are receiving data from the API
def test_eligibility_pass():
    payload = {
        "age": 35,
        "income": 80000,
        "employment_status": "employed"
    }
    response = client.post("/loan-eligibility", json=payload)
    assert response.status_code == 200
    assert response.json() == {"eligible": True}


def test_eligibility_fail():
    payload = {
        "age": 20,
        "income": 40000,
        "employment_status": "unemployed"
    }
    response = client.post("/loan-eligibility", json=payload)
    assert response.status_code == 200
    assert response.json() == {"eligible": False}


