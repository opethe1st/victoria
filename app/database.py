import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

# Get the project root directory (parent of app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'victoria.db')


def get_db_connection():
    """Create a database connection."""
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            upload_date TIMESTAMP NOT NULL,
            activity_date TIMESTAMP NOT NULL,
            duration INTEGER NOT NULL,
            total_distance REAL NOT NULL,
            avg_heart_rate INTEGER,
            file_path TEXT NOT NULL
        )
    ''')

    # GPS Points table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gps_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            latitude REAL,
            longitude REAL,
            distance REAL NOT NULL,
            speed REAL,
            heart_rate INTEGER,
            FOREIGN KEY (activity_id) REFERENCES activities (id) ON DELETE CASCADE
        )
    ''')

    # Personal Bests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_bests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            distance REAL NOT NULL,
            best_time INTEGER NOT NULL,
            avg_pace REAL NOT NULL,
            activity_id INTEGER NOT NULL,
            achieved_date TIMESTAMP NOT NULL,
            FOREIGN KEY (activity_id) REFERENCES activities (id) ON DELETE CASCADE,
            UNIQUE(activity_type, distance)
        )
    ''')

    # Time Aggregations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_aggregations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            date DATE NOT NULL,
            duration INTEGER NOT NULL,
            aggregation_type TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


class Activity:
    """Model for fitness activities."""

    @staticmethod
    def create(activity_type: str, activity_date: datetime, duration: int,
               total_distance: float, file_path: str, avg_heart_rate: Optional[int] = None) -> int:
        """Create a new activity record."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activities (activity_type, upload_date, activity_date,
                                   duration, total_distance, avg_heart_rate, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (activity_type, datetime.now(), activity_date, duration,
              total_distance, avg_heart_rate, file_path))
        activity_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return activity_id

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all activities."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM activities ORDER BY activity_date DESC')
        activities = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return activities

    @staticmethod
    def get_by_id(activity_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific activity by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
        activity = cursor.fetchone()
        conn.close()
        return dict(activity) if activity else None


class GPSPoint:
    """Model for GPS tracking points."""

    @staticmethod
    def create_batch(activity_id: int, points: List[Dict[str, Any]]):
        """Create multiple GPS points for an activity."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO gps_points (activity_id, timestamp, latitude, longitude,
                                   distance, speed, heart_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', [(activity_id, p['timestamp'], p.get('latitude'), p.get('longitude'),
               p['distance'], p.get('speed'), p.get('heart_rate')) for p in points])
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_activity(activity_id: int) -> List[Dict[str, Any]]:
        """Get all GPS points for a specific activity."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gps_points WHERE activity_id = ? ORDER BY timestamp',
                      (activity_id,))
        points = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return points


class PersonalBest:
    """Model for personal best records."""

    @staticmethod
    def upsert(activity_type: str, distance: float, best_time: int,
               avg_pace: float, activity_id: int, achieved_date: datetime):
        """Create or update a personal best record."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO personal_bests (activity_type, distance, best_time,
                                       avg_pace, activity_id, achieved_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(activity_type, distance)
            DO UPDATE SET best_time = excluded.best_time,
                         avg_pace = excluded.avg_pace,
                         activity_id = excluded.activity_id,
                         achieved_date = excluded.achieved_date
            WHERE excluded.best_time < best_time
        ''', (activity_type, distance, best_time, avg_pace, activity_id, achieved_date))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_type(activity_type: str) -> List[Dict[str, Any]]:
        """Get all personal bests for a specific activity type."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM personal_bests
            WHERE activity_type = ?
            ORDER BY distance
        ''', (activity_type,))
        pbs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return pbs

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all personal bests."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personal_bests ORDER BY activity_type, distance')
        pbs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return pbs
