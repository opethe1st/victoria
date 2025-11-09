"""
Personal Best service - Business logic for personal best operations.
"""
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories import PersonalBestRepository


class PersonalBestService:
    """Service for personal best-related business logic."""

    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.pb_repo = PersonalBestRepository(db)

    def upsert_personal_best(
        self,
        activity_type: str,
        distance: float,
        best_time: int,
        avg_pace: float,
        activity_id: int,
        achieved_date: datetime
    ) -> None:
        """
        Create or update a personal best record.

        Only updates if the new time is better than the existing one.
        """
        try:
            existing = self.pb_repo.get_by_type_and_distance(activity_type, distance)

            if existing:
                # Only update if new time is better (lower)
                if best_time < existing.best_time:
                    self.pb_repo.update(
                        existing,
                        best_time=best_time,
                        avg_pace=avg_pace,
                        activity_id=activity_id,
                        achieved_date=achieved_date
                    )
            else:
                # Create new PB record
                self.pb_repo.create(
                    activity_type=activity_type,
                    distance=distance,
                    best_time=best_time,
                    avg_pace=avg_pace,
                    activity_id=activity_id,
                    achieved_date=achieved_date
                )

            # Commit the transaction
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def get_all_personal_bests(self) -> List[Dict[str, Any]]:
        """Get all personal bests as dictionaries."""
        pbs = self.pb_repo.get_all()
        return [self._to_dict(pb) for pb in pbs]

    def get_personal_bests_by_type(self, activity_type: str) -> List[Dict[str, Any]]:
        """Get all personal bests for a specific activity type."""
        pbs = self.pb_repo.get_by_type(activity_type)
        return [self._to_dict(pb) for pb in pbs]

    @staticmethod
    def _to_dict(pb) -> Dict[str, Any]:
        """Convert personal best model to dictionary."""
        return {
            'id': pb.id,
            'activity_type': pb.activity_type,
            'distance': pb.distance,
            'best_time': pb.best_time,
            'avg_pace': pb.avg_pace,
            'activity_id': pb.activity_id,
            'achieved_date': pb.achieved_date.isoformat() if pb.achieved_date else None
        }
