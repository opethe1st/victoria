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


# Helper functions for compatibility with existing code
class Activity:
    """Helper class to maintain compatibility with existing code."""

    @staticmethod
    def create(activity_type: str, activity_date: datetime, duration: int,
               total_distance: float, file_path: str, avg_heart_rate: Optional[int] = None) -> int:
        """Create a new activity record."""
        db = SessionLocal()
        try:
            activity = ActivityModel(
                activity_type=activity_type,
                upload_date=datetime.now(),
                activity_date=activity_date,
                duration=duration,
                total_distance=total_distance,
                avg_heart_rate=avg_heart_rate,
                file_path=file_path
            )
            db.add(activity)
            db.commit()
            db.refresh(activity)
            return activity.id
        finally:
            db.close()

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all activities."""
        db = SessionLocal()
        try:
            activities = db.query(ActivityModel).order_by(ActivityModel.activity_date.desc()).all()
            return [
                {
                    'id': a.id,
                    'activity_type': a.activity_type,
                    'upload_date': a.upload_date.isoformat() if a.upload_date else None,
                    'activity_date': a.activity_date.isoformat() if a.activity_date else None,
                    'duration': a.duration,
                    'total_distance': a.total_distance,
                    'avg_heart_rate': a.avg_heart_rate,
                    'file_path': a.file_path
                }
                for a in activities
            ]
        finally:
            db.close()

    @staticmethod
    def get_by_id(activity_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific activity by ID."""
        db = SessionLocal()
        try:
            activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
            if not activity:
                return None
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
        finally:
            db.close()


class GPSPoint:
    """Helper class for GPS points."""

    @staticmethod
    def create_batch(activity_id: int, points: List[Dict[str, Any]]):
        """Create multiple GPS points for an activity."""
        db = SessionLocal()
        try:
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
            db.add_all(gps_points)
            db.commit()
        finally:
            db.close()

    @staticmethod
    def get_by_activity(activity_id: int) -> List[Dict[str, Any]]:
        """Get all GPS points for a specific activity."""
        db = SessionLocal()
        try:
            points = db.query(GPSPointModel).filter(
                GPSPointModel.activity_id == activity_id
            ).order_by(GPSPointModel.timestamp).all()
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
    """Helper class for personal bests."""

    @staticmethod
    def upsert(activity_type: str, distance: float, best_time: int,
               avg_pace: float, activity_id: int, achieved_date: datetime):
        """Create or update a personal best record."""
        db = SessionLocal()
        try:
            existing = db.query(PersonalBestModel).filter(
                PersonalBestModel.activity_type == activity_type,
                PersonalBestModel.distance == distance
            ).first()

            if existing:
                if best_time < existing.best_time:
                    existing.best_time = best_time
                    existing.avg_pace = avg_pace
                    existing.activity_id = activity_id
                    existing.achieved_date = achieved_date
            else:
                pb = PersonalBestModel(
                    activity_type=activity_type,
                    distance=distance,
                    best_time=best_time,
                    avg_pace=avg_pace,
                    activity_id=activity_id,
                    achieved_date=achieved_date
                )
                db.add(pb)
            db.commit()
        finally:
            db.close()

    @staticmethod
    def get_by_type(activity_type: str) -> List[Dict[str, Any]]:
        """Get all personal bests for a specific activity type."""
        db = SessionLocal()
        try:
            pbs = db.query(PersonalBestModel).filter(
                PersonalBestModel.activity_type == activity_type
            ).order_by(PersonalBestModel.distance).all()
            return [
                {
                    'id': pb.id,
                    'activity_type': pb.activity_type,
                    'distance': pb.distance,
                    'best_time': pb.best_time,
                    'avg_pace': pb.avg_pace,
                    'activity_id': pb.activity_id,
                    'achieved_date': pb.achieved_date.isoformat() if pb.achieved_date else None
                }
                for pb in pbs
            ]
        finally:
            db.close()

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all personal bests."""
        db = SessionLocal()
        try:
            pbs = db.query(PersonalBestModel).order_by(
                PersonalBestModel.activity_type,
                PersonalBestModel.distance
            ).all()
            return [
                {
                    'id': pb.id,
                    'activity_type': pb.activity_type,
                    'distance': pb.distance,
                    'best_time': pb.best_time,
                    'avg_pace': pb.avg_pace,
                    'activity_id': pb.activity_id,
                    'achieved_date': pb.achieved_date.isoformat() if pb.achieved_date else None
                }
                for pb in pbs
            ]
        finally:
            db.close()
