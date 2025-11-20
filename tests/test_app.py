import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app
from src.activities_data import activities, get_initial_activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(get_initial_activities()))

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

    # Try unregistering again (should fail)
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
