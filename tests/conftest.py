"""
Pytest configuration and fixtures for testing.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from datetime import datetime


@pytest.fixture(scope="function")
def test_db():
    """
    Create a test database for each test function.
    Uses an in-memory SQLite database for fast, isolated tests.
    """
    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a session
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_activity_data():
    """Sample activity data for testing."""
    return {
        'activity_type': 'running',
        'activity_date': datetime(2024, 1, 15, 10, 30),
        'duration': 3600,  # 1 hour
        'total_distance': 10000.0,  # 10km
        'file_path': 'uploads/test_activity.fit',
        'avg_heart_rate': 150
    }


@pytest.fixture
def sample_gps_points():
    """Sample GPS point data for testing."""
    return [
        {
            'timestamp': datetime(2024, 1, 15, 10, 30),
            'latitude': 37.7749,
            'longitude': -122.4194,
            'distance': 0.0,
            'speed': 0.0,
            'heart_rate': 145
        },
        {
            'timestamp': datetime(2024, 1, 15, 10, 31),
            'latitude': 37.7750,
            'longitude': -122.4195,
            'distance': 100.0,
            'speed': 2.5,
            'heart_rate': 150
        },
        {
            'timestamp': datetime(2024, 1, 15, 10, 32),
            'latitude': 37.7751,
            'longitude': -122.4196,
            'distance': 200.0,
            'speed': 2.6,
            'heart_rate': 155
        }
    ]


@pytest.fixture
def sample_personal_best_data():
    """Sample personal best data for testing."""
    return {
        'activity_type': 'running',
        'distance': 5000.0,  # 5km
        'best_time': 1500,  # 25 minutes
        'avg_pace': 5.0,  # min/km
        'achieved_date': datetime(2024, 1, 15, 10, 30)
    }
