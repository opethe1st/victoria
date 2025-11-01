"""
Activity repository - handles all database operations for activities.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import ActivityModel


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
        activity = ActivityModel(
            activity_type=activity_type,
            upload_date=datetime.now(),
            activity_date=activity_date,
            duration=duration,
            total_distance=total_distance,
            avg_heart_rate=avg_heart_rate,
            file_path=file_path
        )
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def get_all(self) -> List[ActivityModel]:
        """Get all activities ordered by activity date descending."""
        return self.db.query(ActivityModel).order_by(
            ActivityModel.activity_date.desc()
        ).all()

    def get_by_id(self, activity_id: int) -> Optional[ActivityModel]:
        """Get a specific activity by ID."""
        return self.db.query(ActivityModel).filter(
            ActivityModel.id == activity_id
        ).first()

    def get_by_type(self, activity_type: str) -> List[ActivityModel]:
        """Get all activities of a specific type."""
        return self.db.query(ActivityModel).filter(
            ActivityModel.activity_type == activity_type
        ).order_by(ActivityModel.activity_date.desc()).all()

    def delete(self, activity_id: int) -> bool:
        """Delete an activity by ID."""
        activity = self.get_by_id(activity_id)
        if activity:
            self.db.delete(activity)
            self.db.commit()
            return True
        return False
