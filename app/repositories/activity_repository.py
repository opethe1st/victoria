"""
Activity repository - handles all database operations for activities.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.database import ActivityModel
from app.validation import (
    validate_activity_type,
    validate_positive_number,
    validate_activity_date,
    validate_file_path
)


class ActivityRepository:
    """Repository for Activity data access."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(
        self,
        activity_type: str,
        activity_date: datetime,
        duration: int,
        total_distance: float,
        file_path: str,
        avg_heart_rate: Optional[int] = None
    ) -> ActivityModel:
        """Create a new activity record."""
        # Validate inputs
        validate_activity_type(activity_type)
        validate_activity_date(activity_date)
        validate_positive_number(duration, "duration")
        validate_positive_number(total_distance, "total_distance")
        validate_file_path(file_path)

        if avg_heart_rate is not None:
            validate_positive_number(avg_heart_rate, "avg_heart_rate")

        activity = ActivityModel(
            activity_type=activity_type.lower(),
            upload_date=datetime.now(),
            activity_date=activity_date,
            duration=duration,
            total_distance=total_distance,
            avg_heart_rate=avg_heart_rate,
            file_path=file_path
        )
        self.db.add(activity)
        self.db.flush()  # Flush to get the ID without committing
        return activity

    def get_all(self, eager_load: bool = False) -> List[ActivityModel]:
        """
        Get all activities ordered by activity date descending.

        Args:
            eager_load: If True, eagerly load GPS points and personal bests to avoid N+1 queries.
        """
        query = self.db.query(ActivityModel)

        if eager_load:
            query = query.options(
                joinedload(ActivityModel.gps_points),
                joinedload(ActivityModel.personal_bests)
            )

        return query.order_by(ActivityModel.activity_date.desc()).all()

    def get_by_id(self, activity_id: int, eager_load: bool = False) -> Optional[ActivityModel]:
        """
        Get a specific activity by ID.

        Args:
            activity_id: The ID of the activity.
            eager_load: If True, eagerly load GPS points and personal bests to avoid N+1 queries.
        """
        query = self.db.query(ActivityModel).filter(ActivityModel.id == activity_id)

        if eager_load:
            query = query.options(
                joinedload(ActivityModel.gps_points),
                joinedload(ActivityModel.personal_bests)
            )

        return query.first()

    def get_by_type(self, activity_type: str, eager_load: bool = False) -> List[ActivityModel]:
        """
        Get all activities of a specific type.

        Args:
            activity_type: The type of activity to filter by.
            eager_load: If True, eagerly load GPS points and personal bests to avoid N+1 queries.
        """
        query = self.db.query(ActivityModel).filter(
            ActivityModel.activity_type == activity_type
        )

        if eager_load:
            query = query.options(
                joinedload(ActivityModel.gps_points),
                joinedload(ActivityModel.personal_bests)
            )

        return query.order_by(ActivityModel.activity_date.desc()).all()

    def delete(self, activity_id: int) -> bool:
        """Delete an activity by ID."""
        activity = self.get_by_id(activity_id)
        if activity:
            self.db.delete(activity)
            # Let service handle commit
            return True
        return False
