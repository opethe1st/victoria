"""
Unit tests for ActivityService.
"""
import pytest
from datetime import datetime
from app.services import ActivityService
from app.repositories import ActivityRepository


class TestActivityService:
    """Tests for ActivityService class."""

    def test_get_all_activities(self, test_db, sample_activity_data):
        """Test getting all activities as dictionaries."""
        service = ActivityService(test_db)

        # Create activities directly through repo
        repo = ActivityRepository(test_db)
        repo.create(**sample_activity_data)
        test_db.commit()

        activities = service.get_all_activities()
        assert len(activities) == 1
        assert isinstance(activities[0], dict)
        assert activities[0]['activity_type'] == sample_activity_data['activity_type']

    def test_get_activity_by_id(self, test_db, sample_activity_data):
        """Test getting a specific activity by ID."""
        service = ActivityService(test_db)
        repo = ActivityRepository(test_db)

        activity = repo.create(**sample_activity_data)
        test_db.commit()

        result = service.get_activity_by_id(activity.id)
        assert result is not None
        assert isinstance(result, dict)
        assert result['id'] == activity.id
        assert result['activity_type'] == sample_activity_data['activity_type']

    def test_get_activity_by_id_not_found(self, test_db):
        """Test getting non-existent activity returns None."""
        service = ActivityService(test_db)
        result = service.get_activity_by_id(9999)
        assert result is None

    def test_get_activities_by_type(self, test_db, sample_activity_data):
        """Test getting activities filtered by type."""
        service = ActivityService(test_db)
        repo = ActivityRepository(test_db)

        # Create running activity
        repo.create(**sample_activity_data)
        test_db.commit()

        # Create cycling activity
        data2 = sample_activity_data.copy()
        data2['activity_type'] = 'cycling'
        repo.create(**data2)
        test_db.commit()

        running_activities = service.get_activities_by_type('running')
        assert len(running_activities) == 1
        assert running_activities[0]['activity_type'] == 'running'

    def test_delete_activity(self, test_db, sample_activity_data):
        """Test deleting an activity through service."""
        service = ActivityService(test_db)
        repo = ActivityRepository(test_db)

        activity = repo.create(**sample_activity_data)
        test_db.commit()

        result = service.delete_activity(activity.id)
        assert result is True

        # Verify it's deleted
        found = service.get_activity_by_id(activity.id)
        assert found is None

    def test_to_dict_conversion(self, test_db, sample_activity_data):
        """Test activity model to dict conversion."""
        service = ActivityService(test_db)
        repo = ActivityRepository(test_db)

        activity = repo.create(**sample_activity_data)
        test_db.commit()

        activity_dict = service._to_dict(activity)

        assert 'id' in activity_dict
        assert 'activity_type' in activity_dict
        assert 'activity_date' in activity_dict
        assert 'upload_date' in activity_dict
        assert 'duration' in activity_dict
        assert 'total_distance' in activity_dict
        assert 'avg_heart_rate' in activity_dict
        assert 'file_path' in activity_dict

        # Check date formatting
        assert isinstance(activity_dict['activity_date'], str)
        assert isinstance(activity_dict['upload_date'], str)
