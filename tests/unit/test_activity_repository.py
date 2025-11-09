"""
Unit tests for ActivityRepository.
"""
import pytest
from datetime import datetime
from app.repositories import ActivityRepository
from app.exceptions import InvalidActivityTypeError


class TestActivityRepository:
    """Tests for ActivityRepository class."""

    def test_create_activity(self, test_db, sample_activity_data):
        """Test creating a new activity."""
        repo = ActivityRepository(test_db)
        activity = repo.create(**sample_activity_data)

        assert activity.id is not None
        assert activity.activity_type == sample_activity_data['activity_type']
        assert activity.duration == sample_activity_data['duration']
        assert activity.total_distance == sample_activity_data['total_distance']
        assert activity.avg_heart_rate == sample_activity_data['avg_heart_rate']

    def test_create_activity_invalid_type(self, test_db):
        """Test creating activity with invalid type raises error."""
        repo = ActivityRepository(test_db)

        with pytest.raises(InvalidActivityTypeError):
            repo.create(
                activity_type='invalid_type',
                activity_date=datetime.now(),
                duration=3600,
                total_distance=10000.0,
                file_path='uploads/test.fit'
            )

    def test_create_activity_negative_duration(self, test_db):
        """Test creating activity with negative duration raises error."""
        repo = ActivityRepository(test_db)

        with pytest.raises(ValueError, match="duration must be non-negative"):
            repo.create(
                activity_type='running',
                activity_date=datetime.now(),
                duration=-100,
                total_distance=10000.0,
                file_path='uploads/test.fit'
            )

    def test_create_activity_negative_distance(self, test_db):
        """Test creating activity with negative distance raises error."""
        repo = ActivityRepository(test_db)

        with pytest.raises(ValueError, match="total_distance must be non-negative"):
            repo.create(
                activity_type='running',
                activity_date=datetime.now(),
                duration=3600,
                total_distance=-1000.0,
                file_path='uploads/test.fit'
            )

    def test_create_activity_future_date(self, test_db):
        """Test creating activity with future date raises error."""
        repo = ActivityRepository(test_db)
        future_date = datetime(2099, 12, 31, 23, 59)

        with pytest.raises(ValueError, match="cannot be in the future"):
            repo.create(
                activity_type='running',
                activity_date=future_date,
                duration=3600,
                total_distance=10000.0,
                file_path='uploads/test.fit'
            )

    def test_get_all_activities(self, test_db, sample_activity_data):
        """Test getting all activities."""
        repo = ActivityRepository(test_db)

        # Create multiple activities
        repo.create(**sample_activity_data)
        test_db.commit()

        data2 = sample_activity_data.copy()
        data2['activity_date'] = datetime(2024, 1, 16, 10, 30)
        repo.create(**data2)
        test_db.commit()

        activities = repo.get_all()
        assert len(activities) == 2
        # Should be ordered by date descending
        assert activities[0].activity_date > activities[1].activity_date

    def test_get_by_id(self, test_db, sample_activity_data):
        """Test getting activity by ID."""
        repo = ActivityRepository(test_db)
        activity = repo.create(**sample_activity_data)
        test_db.commit()

        found = repo.get_by_id(activity.id)
        assert found is not None
        assert found.id == activity.id
        assert found.activity_type == activity.activity_type

    def test_get_by_id_not_found(self, test_db):
        """Test getting non-existent activity returns None."""
        repo = ActivityRepository(test_db)
        found = repo.get_by_id(9999)
        assert found is None

    def test_get_by_type(self, test_db, sample_activity_data):
        """Test getting activities by type."""
        repo = ActivityRepository(test_db)

        # Create running activity
        repo.create(**sample_activity_data)
        test_db.commit()

        # Create cycling activity
        data2 = sample_activity_data.copy()
        data2['activity_type'] = 'cycling'
        repo.create(**data2)
        test_db.commit()

        running_activities = repo.get_by_type('running')
        assert len(running_activities) == 1
        assert running_activities[0].activity_type == 'running'

        cycling_activities = repo.get_by_type('cycling')
        assert len(cycling_activities) == 1
        assert cycling_activities[0].activity_type == 'cycling'

    def test_delete_activity(self, test_db, sample_activity_data):
        """Test deleting an activity."""
        repo = ActivityRepository(test_db)
        activity = repo.create(**sample_activity_data)
        test_db.commit()

        activity_id = activity.id
        result = repo.delete(activity_id)
        test_db.commit()

        assert result is True
        assert repo.get_by_id(activity_id) is None

    def test_delete_non_existent_activity(self, test_db):
        """Test deleting non-existent activity returns False."""
        repo = ActivityRepository(test_db)
        result = repo.delete(9999)
        assert result is False
