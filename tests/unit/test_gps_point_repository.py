"""
Unit tests for GPSPointRepository.
"""
import pytest
from app.repositories import GPSPointRepository, ActivityRepository


class TestGPSPointRepository:
    """Tests for GPSPointRepository class."""

    def test_create_batch(self, test_db, sample_activity_data, sample_gps_points):
        """Test creating GPS points in batch."""
        # Create activity first
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        # Create GPS points
        gps_repo = GPSPointRepository(test_db)
        gps_repo.create_batch(activity.id, sample_gps_points)
        test_db.commit()

        # Verify they were created
        points = gps_repo.get_by_activity(activity.id)
        assert len(points) == len(sample_gps_points)

    def test_get_by_activity(self, test_db, sample_activity_data, sample_gps_points):
        """Test getting GPS points for an activity."""
        # Create activity and GPS points
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        gps_repo = GPSPointRepository(test_db)
        gps_repo.create_batch(activity.id, sample_gps_points)
        test_db.commit()

        # Get points
        points = gps_repo.get_by_activity(activity.id)
        assert len(points) == 3
        # Should be ordered by timestamp
        assert points[0].timestamp <= points[1].timestamp <= points[2].timestamp

    def test_get_by_activity_no_points(self, test_db, sample_activity_data):
        """Test getting GPS points for activity with no points."""
        # Create activity without GPS points
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        gps_repo = GPSPointRepository(test_db)
        points = gps_repo.get_by_activity(activity.id)
        assert len(points) == 0

    def test_delete_by_activity(self, test_db, sample_activity_data, sample_gps_points):
        """Test deleting all GPS points for an activity."""
        # Create activity and GPS points
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        gps_repo = GPSPointRepository(test_db)
        gps_repo.create_batch(activity.id, sample_gps_points)
        test_db.commit()

        # Delete all points
        gps_repo.delete_by_activity(activity.id)
        test_db.commit()

        # Verify they're gone
        points = gps_repo.get_by_activity(activity.id)
        assert len(points) == 0

    def test_gps_point_fields(self, test_db, sample_activity_data, sample_gps_points):
        """Test that GPS point fields are stored correctly."""
        # Create activity and GPS points
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        gps_repo = GPSPointRepository(test_db)
        gps_repo.create_batch(activity.id, sample_gps_points)
        test_db.commit()

        points = gps_repo.get_by_activity(activity.id)
        first_point = points[0]

        assert first_point.activity_id == activity.id
        assert first_point.latitude == sample_gps_points[0]['latitude']
        assert first_point.longitude == sample_gps_points[0]['longitude']
        assert first_point.distance == sample_gps_points[0]['distance']
        assert first_point.speed == sample_gps_points[0]['speed']
        assert first_point.heart_rate == sample_gps_points[0]['heart_rate']
