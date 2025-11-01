"""
Personal Best repository - handles all database operations for personal bests.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import PersonalBestModel


class PersonalBestRepository:
    """Repository for Personal Best data access."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def get_by_type_and_distance(
        self, activity_type: str, distance: float
    ) -> Optional[PersonalBestModel]:
        """Get a personal best for a specific activity type and distance."""
        return self.db.query(PersonalBestModel).filter(
            PersonalBestModel.activity_type == activity_type,
            PersonalBestModel.distance == distance
        ).first()

    def create(
        self,
        activity_type: str,
        distance: float,
        best_time: int,
        avg_pace: float,
        activity_id: int,
        achieved_date: datetime
    ) -> PersonalBestModel:
        """Create a new personal best record."""
        pb = PersonalBestModel(
            activity_type=activity_type,
            distance=distance,
            best_time=best_time,
            avg_pace=avg_pace,
            activity_id=activity_id,
            achieved_date=achieved_date
        )
        self.db.add(pb)
        self.db.commit()
        self.db.refresh(pb)
        return pb

    def update(
        self,
        pb: PersonalBestModel,
        best_time: int,
        avg_pace: float,
        activity_id: int,
        achieved_date: datetime
    ) -> PersonalBestModel:
        """Update an existing personal best record."""
        pb.best_time = best_time
        pb.avg_pace = avg_pace
        pb.activity_id = activity_id
        pb.achieved_date = achieved_date
        self.db.commit()
        self.db.refresh(pb)
        return pb

    def get_by_type(self, activity_type: str) -> List[PersonalBestModel]:
        """Get all personal bests for a specific activity type."""
        return self.db.query(PersonalBestModel).filter(
            PersonalBestModel.activity_type == activity_type
        ).order_by(PersonalBestModel.distance).all()

    def get_all(self) -> List[PersonalBestModel]:
        """Get all personal bests."""
        return self.db.query(PersonalBestModel).order_by(
            PersonalBestModel.activity_type,
            PersonalBestModel.distance
        ).all()
