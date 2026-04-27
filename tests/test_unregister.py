import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestUnregister:
    def test_unregister_success(self):
        # Arrange
        client = TestClient(app)
        activity_name = "Gym Class"
        email = "unregister@example.com"

        # First signup
        client.post(f"/activities/{activity_name}/signup?email={email}")
        assert email in activities[activity_name]["participants"]

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        # Verify participant was removed
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_activity(self):
        # Arrange
        client = TestClient(app)
        activity_name = "Nonexistent Activity"
        email = "student@example.com"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unregister_nonexistent_participant(self):
        # Arrange
        client = TestClient(app)
        activity_name = "Basketball Team"
        email = "notsignedup@example.com"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower() or "not found" in data["detail"].lower()