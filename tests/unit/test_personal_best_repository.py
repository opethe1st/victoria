"""
Unit tests for PersonalBestRepository.
"""
import pytest
from datetime import datetime
from app.repositories import PersonalBestRepository, ActivityRepository
from app.exceptions import InvalidActivityTypeError


class TestPersonalBestRepository:
    """Tests for PersonalBestRepository class."""

    def test_create_personal_best(self, test_db, sample_activity_data, sample_personal_best_data):
        """Test creating a new personal best."""
        # Create an activity first
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        # Create personal best
        pb_repo = PersonalBestRepository(test_db)
        pb = pb_repo.create(
            activity_id=activity.id,
            **sample_personal_best_data
        )

        assert pb.id is not None
        assert pb.activity_type == sample_personal_best_data['activity_type']
        assert pb.distance == sample_personal_best_data['distance']
        assert pb.best_time == sample_personal_best_data['best_time']
        assert pb.activity_id == activity.id

    def test_create_personal_best_invalid_type(self, test_db):
        """Test creating PB with invalid type raises error."""
        pb_repo = PersonalBestRepository(test_db)

        with pytest.raises(InvalidActivityTypeError):
            pb_repo.create(
                activity_type='invalid_type',
                distance=5000.0,
                best_time=1500,
                avg_pace=5.0,
                activity_id=1,
                achieved_date=datetime.now()
            )

    def test_create_personal_best_negative_values(self, test_db):
        """Test creating PB with negative values raises error."""
        pb_repo = PersonalBestRepository(test_db)

        with pytest.raises(ValueError, match="distance must be non-negative"):
            pb_repo.create(
                activity_type='running',
                distance=-5000.0,
                best_time=1500,
                avg_pace=5.0,
                activity_id=1,
                achieved_date=datetime.now()
            )

    def test_get_by_type_and_distance(self, test_db, sample_activity_data, sample_personal_best_data):
        """Test getting PB by type and distance."""
        # Create activity and PB
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        pb_repo = PersonalBestRepository(test_db)
        pb = pb_repo.create(activity_id=activity.id, **sample_personal_best_data)
        test_db.commit()

        # Find it
        found = pb_repo.get_by_type_and_distance('running', 5000.0)
        assert found is not None
        assert found.id == pb.id

    def test_update_personal_best(self, test_db, sample_activity_data, sample_personal_best_data):
        """Test updating a personal best."""
        # Create activity and PB
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        pb_repo = PersonalBestRepository(test_db)
        pb = pb_repo.create(activity_id=activity.id, **sample_personal_best_data)
        test_db.commit()

        # Update it
        new_time = 1400  # Improved time
        updated_pb = pb_repo.update(
            pb=pb,
            best_time=new_time,
            avg_pace=4.67,
            activity_id=activity.id,
            achieved_date=datetime.now()
        )

        assert updated_pb.best_time == new_time

    def test_get_by_type(self, test_db, sample_activity_data, sample_personal_best_data):
        """Test getting all PBs for a type."""
        # Create activity
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        # Create multiple PBs
        pb_repo = PersonalBestRepository(test_db)
        pb_repo.create(activity_id=activity.id, **sample_personal_best_data)

        data2 = sample_personal_best_data.copy()
        data2['distance'] = 10000.0
        data2['best_time'] = 3000
        pb_repo.create(activity_id=activity.id, **data2)
        test_db.commit()

        pbs = pb_repo.get_by_type('running')
        assert len(pbs) == 2
        # Should be ordered by distance
        assert pbs[0].distance < pbs[1].distance

    def test_get_all(self, test_db, sample_activity_data, sample_personal_best_data):
        """Test getting all personal bests."""
        # Create activity
        activity_repo = ActivityRepository(test_db)
        activity = activity_repo.create(**sample_activity_data)
        test_db.commit()

        # Create PBs for different types
        pb_repo = PersonalBestRepository(test_db)
        pb_repo.create(activity_id=activity.id, **sample_personal_best_data)

        data2 = sample_personal_best_data.copy()
        data2['activity_type'] = 'cycling'
        pb_repo.create(activity_id=activity.id, **data2)
        test_db.commit()

        all_pbs = pb_repo.get_all()
        assert len(all_pbs) == 2
