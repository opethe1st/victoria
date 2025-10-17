"""
FIT file parser for extracting activity data from .fit files.
"""
from fitparse import FitFile
from datetime import datetime
from typing import Dict, List, Optional, Any


def parse_fit_file(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Parse a .fit file and extract activity data.

    Returns a dictionary with:
    - activity_type: str (swimming, cycling, running)
    - activity_date: datetime
    - duration: int (seconds)
    - total_distance: float (meters)
    - avg_heart_rate: Optional[int]
    - gps_points: List[Dict] with timestamp, lat, lon, distance, speed, heart_rate
    """
    try:
        fitfile = FitFile(filepath)

        # Extract session data (summary information)
        session_data = None
        for record in fitfile.get_messages('session'):
            session_data = record
            break

        if not session_data:
            return None

        # Extract key fields from session
        sport = None
        start_time = None
        total_elapsed_time = 0
        total_distance = 0.0
        avg_heart_rate = None

        for field in session_data:
            if field.name == 'sport':
                sport = field.value
            elif field.name == 'start_time':
                start_time = field.value
            elif field.name == 'total_elapsed_time':
                total_elapsed_time = field.value
            elif field.name == 'total_distance':
                total_distance = field.value
            elif field.name == 'avg_heart_rate':
                avg_heart_rate = field.value

        # Map sport type to our activity types
        activity_type_map = {
            'swimming': 'swimming',
            'cycling': 'cycling',
            'running': 'running',
            'lap_swimming': 'swimming',
            'open_water_swimming': 'swimming',
            'generic': 'running',  # Default fallback
        }

        activity_type = activity_type_map.get(sport.lower() if sport else 'generic', 'running')

        # Extract GPS points (record messages)
        gps_points = []
        cumulative_distance = 0.0

        for record in fitfile.get_messages('record'):
            point = {}
            for field in record:
                if field.name == 'timestamp':
                    point['timestamp'] = field.value
                elif field.name == 'position_lat':
                    # Convert from semicircles to degrees
                    if field.value is not None:
                        point['latitude'] = field.value * (180.0 / 2**31)
                elif field.name == 'position_long':
                    # Convert from semicircles to degrees
                    if field.value is not None:
                        point['longitude'] = field.value * (180.0 / 2**31)
                elif field.name == 'distance':
                    cumulative_distance = field.value
                    point['distance'] = field.value
                elif field.name == 'speed':
                    point['speed'] = field.value
                elif field.name == 'heart_rate':
                    point['heart_rate'] = field.value

            # Only add points with timestamp
            if 'timestamp' in point:
                if 'distance' not in point:
                    point['distance'] = cumulative_distance
                gps_points.append(point)

        return {
            'activity_type': activity_type,
            'activity_date': start_time or datetime.now(),
            'duration': int(total_elapsed_time) if total_elapsed_time else 0,
            'total_distance': total_distance if total_distance else 0.0,
            'avg_heart_rate': int(avg_heart_rate) if avg_heart_rate else None,
            'gps_points': gps_points
        }

    except Exception as e:
        print(f"Error parsing FIT file {filepath}: {e}")
        return None
