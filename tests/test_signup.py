import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestSignup:
    def test_signup_success(self):
        # Arrange
        client = TestClient(app)
        activity_name = "Chess Club"
        email = "student@example.com"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        # Verify participant was added
        assert email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity(self):
        # Arrange
        client = TestClient(app)
        activity_name = "Nonexistent Activity"
        email = "student@example.com"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_email(self):
        # Arrange
        client = TestClient(app)
        activity_name = "Programming Class"
        email = "duplicate@example.com"

        # First signup
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act - Second signup with same email
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower() or "duplicate" in data["detail"].lower()