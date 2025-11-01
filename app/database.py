from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.config import Config

# Create database engine
engine = create_engine(Config.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy Models
class ActivityModel(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False)
    activity_date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # seconds
    total_distance = Column(Float, nullable=False)  # meters
    avg_heart_rate = Column(Integer, nullable=True)
    file_path = Column(String, nullable=False)

    gps_points = relationship("GPSPointModel", back_populates="activity", cascade="all, delete-orphan")
    personal_bests = relationship("PersonalBestModel", back_populates="activity", cascade="all, delete-orphan")


class GPSPointModel(Base):
    __tablename__ = "gps_points"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    distance = Column(Float, nullable=False)  # cumulative meters
    speed = Column(Float, nullable=True)  # m/s
    heart_rate = Column(Integer, nullable=True)

    activity = relationship("ActivityModel", back_populates="gps_points")


class PersonalBestModel(Base):
    __tablename__ = "personal_bests"

    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String, nullable=False)
    distance = Column(Float, nullable=False)  # meters
    best_time = Column(Integer, nullable=False)  # seconds
    avg_pace = Column(Float, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    achieved_date = Column(DateTime, nullable=False)

    activity = relationship("ActivityModel", back_populates="personal_bests")


class TimeAggregationModel(Base):
    __tablename__ = "time_aggregations"

    id = Column(Integer, primary_key=True, index=True)
    activity_type = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # seconds
    aggregation_type = Column(String, nullable=False)  # 'daily', 'weekly', 'monthly'


def init_db():
    """Initialize the database - create all tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Legacy helper classes for backward compatibility
# TODO: Remove these once all code is migrated to use services
class Activity:
    """Deprecated: Use ActivityService instead."""

    @staticmethod
    def create(activity_type: str, activity_date: datetime, duration: int,
               total_distance: float, file_path: str, avg_heart_rate: Optional[int] = None) -> int:
        """Deprecated: Use ActivityService.create_from_fit_file() instead."""
        from app.services import ActivityService
        db = SessionLocal()
        try:
            service = ActivityService(db)
            from app.repositories import ActivityRepository
            repo = ActivityRepository(db)
            activity = repo.create(activity_type, activity_date, duration, total_distance, file_path, avg_heart_rate)
            return activity.id
        finally:
            db.close()

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Deprecated: Use ActivityService.get_all_activities() instead."""
        from app.services import ActivityService
        db = SessionLocal()
        try:
            service = ActivityService(db)
            return service.get_all_activities()
        finally:
            db.close()

    @staticmethod
    def get_by_id(activity_id: int) -> Optional[Dict[str, Any]]:
        """Deprecated: Use ActivityService.get_activity_by_id() instead."""
        from app.services import ActivityService
        db = SessionLocal()
        try:
            service = ActivityService(db)
            return service.get_activity_by_id(activity_id)
        finally:
            db.close()


class GPSPoint:
    """Deprecated: Use GPSPointRepository instead."""

    @staticmethod
    def create_batch(activity_id: int, points: List[Dict[str, Any]]):
        """Deprecated: Use GPSPointRepository.create_batch() instead."""
        from app.repositories import GPSPointRepository
        db = SessionLocal()
        try:
            repo = GPSPointRepository(db)
            repo.create_batch(activity_id, points)
        finally:
            db.close()

    @staticmethod
    def get_by_activity(activity_id: int) -> List[Dict[str, Any]]:
        """Deprecated: Use GPSPointRepository.get_by_activity() instead."""
        from app.repositories import GPSPointRepository
        db = SessionLocal()
        try:
            repo = GPSPointRepository(db)
            points = repo.get_by_activity(activity_id)
            return [
                {
                    'id': p.id,
                    'activity_id': p.activity_id,
                    'timestamp': p.timestamp.isoformat() if p.timestamp else None,
                    'latitude': p.latitude,
                    'longitude': p.longitude,
                    'distance': p.distance,
                    'speed': p.speed,
                    'heart_rate': p.heart_rate
                }
                for p in points
            ]
        finally:
            db.close()


class PersonalBest:
    """Deprecated: Use PersonalBestService instead."""

    @staticmethod
    def upsert(activity_type: str, distance: float, best_time: int,
               avg_pace: float, activity_id: int, achieved_date: datetime):
        """Deprecated: Use PersonalBestService.upsert_personal_best() instead."""
        from app.services import PersonalBestService
        db = SessionLocal()
        try:
            service = PersonalBestService(db)
            service.upsert_personal_best(activity_type, distance, best_time, avg_pace, activity_id, achieved_date)
        finally:
            db.close()

    @staticmethod
    def get_by_type(activity_type: str) -> List[Dict[str, Any]]:
        """Deprecated: Use PersonalBestService.get_personal_bests_by_type() instead."""
        from app.services import PersonalBestService
        db = SessionLocal()
        try:
            service = PersonalBestService(db)
            return service.get_personal_bests_by_type(activity_type)
        finally:
            db.close()

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Deprecated: Use PersonalBestService.get_all_personal_bests() instead."""
        from app.services import PersonalBestService
        db = SessionLocal()
        try:
            service = PersonalBestService(db)
            return service.get_all_personal_bests()
        finally:
            db.close()
