"""
Input validation utilities.
"""
from datetime import datetime
from typing import Optional
import os
from app.exceptions import InvalidActivityTypeError


# Allowed activity types
VALID_ACTIVITY_TYPES = {
    'running', 'cycling', 'swimming', 'walking',
    'hiking', 'yoga', 'strength', 'other'
}


def validate_activity_type(activity_type: str) -> None:
    """
    Validate that activity type is in the allowed list.

    Raises:
        InvalidActivityTypeError: If activity type is not valid.
    """
    if not activity_type or activity_type.lower() not in VALID_ACTIVITY_TYPES:
        raise InvalidActivityTypeError(
            f"Invalid activity type '{activity_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_ACTIVITY_TYPES))}"
        )


def validate_positive_number(value: float, field_name: str) -> None:
    """
    Validate that a number is positive.

    Raises:
        ValueError: If value is negative.
    """
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative, got {value}")


def validate_activity_date(activity_date: datetime) -> None:
    """
    Validate that activity date is not in the future.

    Raises:
        ValueError: If date is in the future.
    """
    if activity_date > datetime.now():
        raise ValueError(
            f"Activity date cannot be in the future: {activity_date.isoformat()}"
        )


def validate_file_path(file_path: str) -> None:
    """
    Validate and sanitize file path.

    Raises:
        ValueError: If file path is invalid or contains path traversal.
    """
    if not file_path:
        raise ValueError("File path cannot be empty")

    # Check for path traversal attempts
    normalized_path = os.path.normpath(file_path)
    if '..' in normalized_path or normalized_path.startswith('/'):
        raise ValueError(f"Invalid file path: {file_path}")

    # Ensure it's a .fit file
    if not file_path.lower().endswith('.fit'):
        raise ValueError(f"File must be a .fit file: {file_path}")
