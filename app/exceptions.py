"""
Custom exceptions for the application.
"""


class ActivityNotFoundError(Exception):
    """Raised when an activity is not found."""
    pass


class PersonalBestNotFoundError(Exception):
    """Raised when a personal best is not found."""
    pass


class FitFileParseError(Exception):
    """Raised when a FIT file cannot be parsed."""
    pass


class InvalidActivityTypeError(Exception):
    """Raised when an invalid activity type is provided."""
    pass
