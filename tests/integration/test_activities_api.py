"""
Integration tests for activities API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from datetime import datetime


@pytest.fixture
def client(test_db):
    """Create a test client with test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


class TestActivitiesAPI:
    """Integration tests for /api/activities endpoints."""

    def test_get_all_activities_empty(self, client):
        """Test getting activities when database is empty."""
        response = client.get("/api/activities")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] == 0
        assert data["data"] == []

    def test_get_activity_not_found(self, client):
        """Test getting non-existent activity returns 404."""
        response = client.get("/api/activities/9999")
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["error"].lower()

    def test_get_all_activities_with_data(self, client, test_db, sample_activity_data):
        """Test getting activities with data in database."""
        from app.repositories import ActivityRepository

        # Add test data
        repo = ActivityRepository(test_db)
        activity = repo.create(**sample_activity_data)
        test_db.commit()

        response = client.get("/api/activities")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["id"] == activity.id

    def test_get_activity_by_id(self, client, test_db, sample_activity_data):
        """Test getting a specific activity by ID."""
        from app.repositories import ActivityRepository

        # Add test data
        repo = ActivityRepository(test_db)
        activity = repo.create(**sample_activity_data)
        test_db.commit()

        response = client.get(f"/api/activities/{activity.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == activity.id
        assert data["data"]["activity_type"] == sample_activity_data["activity_type"]
