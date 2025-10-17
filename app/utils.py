"""
Utility functions for calculations and formatting.
"""


def calculate_pace_or_speed(activity_type: str, distance_meters: float, duration_seconds: int) -> dict:
    """
    Calculate pace or speed based on activity type.

    Returns a dict with:
    - value: float (the calculated value)
    - unit: str (the unit to display)
    - label: str (what it represents: "Pace" or "Speed")
    """
    if duration_seconds == 0 or distance_meters == 0:
        return {"value": 0, "unit": "", "label": ""}

    if activity_type == "swimming":
        # Swimming: pace per 100m in minutes
        pace_per_100m = (duration_seconds / 60) / (distance_meters / 100)
        return {
            "value": pace_per_100m,
            "unit": "min/100m",
            "label": "Pace"
        }
    elif activity_type == "cycling":
        # Cycling: speed in km/h
        speed_kmh = (distance_meters / 1000) / (duration_seconds / 3600)
        return {
            "value": speed_kmh,
            "unit": "km/h",
            "label": "Speed"
        }
    else:  # running
        # Running: pace per km in minutes
        pace_per_km = (duration_seconds / 60) / (distance_meters / 1000)
        return {
            "value": pace_per_km,
            "unit": "min/km",
            "label": "Pace"
        }


def format_duration(seconds: int) -> str:
    """Format duration in seconds to HH:MM:SS or MM:SS format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def format_distance(meters: float, activity_type: str = None) -> str:
    """Format distance based on activity type."""
    if activity_type == "swimming":
        # Swimming: show in meters
        return f"{int(meters)} m"
    else:
        # Cycling and Running: show in km
        return f"{meters / 1000:.2f} km"
