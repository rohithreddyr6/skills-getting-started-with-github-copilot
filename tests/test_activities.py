import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestGetActivities:
    def test_get_all_activities_success(self):
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # Based on the 9 pre-populated activities
        # Check that all expected activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Soccer Club", "Art Club", "Drama Club", "Debate Club", "Science Club"
        ]
        for activity in expected_activities:
            assert activity in data
            assert "description" in data[activity]
            assert "schedule" in data[activity]
            assert "max_participants" in data[activity]
            assert "participants" in data[activity]
            assert isinstance(data[activity]["participants"], list)