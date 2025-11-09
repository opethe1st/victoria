"""
Error handlers for the application.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import (
    ActivityNotFoundError,
    PersonalBestNotFoundError,
    FitFileParseError,
    InvalidActivityTypeError
)


async def activity_not_found_handler(request: Request, exc: ActivityNotFoundError):
    """Handle ActivityNotFoundError."""
    return JSONResponse(
        status_code=404,
        content={"success": False, "error": "Activity not found"}
    )


async def personal_best_not_found_handler(request: Request, exc: PersonalBestNotFoundError):
    """Handle PersonalBestNotFoundError."""
    return JSONResponse(
        status_code=404,
        content={"success": False, "error": "Personal best not found"}
    )


async def fit_file_parse_handler(request: Request, exc: FitFileParseError):
    """Handle FitFileParseError."""
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": "Failed to parse FIT file"}
    )


async def invalid_activity_type_handler(request: Request, exc: InvalidActivityTypeError):
    """Handle InvalidActivityTypeError."""
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": str(exc)}
    )


def register_error_handlers(app):
    """Register all error handlers with the FastAPI app."""
    app.add_exception_handler(ActivityNotFoundError, activity_not_found_handler)
    app.add_exception_handler(PersonalBestNotFoundError, personal_best_not_found_handler)
    app.add_exception_handler(FitFileParseError, fit_file_parse_handler)
    app.add_exception_handler(InvalidActivityTypeError, invalid_activity_type_handler)
