"""
GPS Point repository - handles all database operations for GPS points.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.database import GPSPointModel


class GPSPointRepository:
    """Repository for GPS Point data access."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create_batch(self, activity_id: int, points: List[Dict[str, Any]]) -> None:
        """Create multiple GPS points for an activity."""
        gps_points = [
            GPSPointModel(
                activity_id=activity_id,
                timestamp=p['timestamp'],
                latitude=p.get('latitude'),
                longitude=p.get('longitude'),
                distance=p['distance'],
                speed=p.get('speed'),
                heart_rate=p.get('heart_rate')
            )
            for p in points
        ]
        self.db.add_all(gps_points)
        # Let service handle commit

    def get_by_activity(self, activity_id: int) -> List[GPSPointModel]:
        """Get all GPS points for a specific activity."""
        return self.db.query(GPSPointModel).filter(
            GPSPointModel.activity_id == activity_id
        ).order_by(GPSPointModel.timestamp).all()

    def delete_by_activity(self, activity_id: int) -> None:
        """Delete all GPS points for a specific activity."""
        self.db.query(GPSPointModel).filter(
            GPSPointModel.activity_id == activity_id
        ).delete()
        # Let service handle commit
