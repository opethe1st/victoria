"""
Activity service - Business logic for activity operations.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories import ActivityRepository, GPSPointRepository
from app.fit_parser import parse_fit_file


class ActivityService:
    """Service for activity-related business logic."""

    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.activity_repo = ActivityRepository(db)
        self.gps_repo = GPSPointRepository(db)

    def create_from_fit_file(self, filepath: str) -> Optional[int]:
        """
        Parse a FIT file and create an activity with GPS points.

        Returns the activity ID if successful, None otherwise.
        """
        # Parse the FIT file
        activity_data = parse_fit_file(filepath)
        if not activity_data:
            return None

        # Create activity record
        activity = self.activity_repo.create(
            activity_type=activity_data['activity_type'],
            activity_date=activity_data['activity_date'],
            duration=activity_data['duration'],
            total_distance=activity_data['total_distance'],
            file_path=filepath,
            avg_heart_rate=activity_data['avg_heart_rate']
        )

        # Store GPS points if available
        if activity_data['gps_points']:
            self.gps_repo.create_batch(activity.id, activity_data['gps_points'])

        return activity.id

    def get_all_activities(self) -> List[Dict[str, Any]]:
        """Get all activities as dictionaries."""
        activities = self.activity_repo.get_all()
        return [self._to_dict(activity) for activity in activities]

    def get_activity_by_id(self, activity_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific activity by ID."""
        activity = self.activity_repo.get_by_id(activity_id)
        if not activity:
            return None
        return self._to_dict(activity)

    def get_activities_by_type(self, activity_type: str) -> List[Dict[str, Any]]:
        """Get all activities of a specific type."""
        activities = self.activity_repo.get_by_type(activity_type)
        return [self._to_dict(activity) for activity in activities]

    def delete_activity(self, activity_id: int) -> bool:
        """Delete an activity and its GPS points."""
        return self.activity_repo.delete(activity_id)

    @staticmethod
    def _to_dict(activity) -> Dict[str, Any]:
        """Convert activity model to dictionary."""
        return {
            'id': activity.id,
            'activity_type': activity.activity_type,
            'upload_date': activity.upload_date.isoformat() if activity.upload_date else None,
            'activity_date': activity.activity_date.isoformat() if activity.activity_date else None,
            'duration': activity.duration,
            'total_distance': activity.total_distance,
            'avg_heart_rate': activity.avg_heart_rate,
            'file_path': activity.file_path
        }
