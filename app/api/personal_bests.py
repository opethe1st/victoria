from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import PersonalBestResponse
from app.database import get_db
from app.services import PersonalBestService
from app.exceptions import InvalidActivityTypeError
from app.validation import VALID_ACTIVITY_TYPES

router = APIRouter()


@router.get("/personal-bests", response_model=dict)
async def get_all_personal_bests(db: Session = Depends(get_db)):
    """
    Get all personal bests across all activity types.

    Returns personal best records for swimming, cycling, and running.
    """
    service = PersonalBestService(db)
    pbs = service.get_all_personal_bests()
    return {
        "success": True,
        "data": pbs,
        "count": len(pbs)
    }


@router.get("/personal-bests/{activity_type}", response_model=dict)
async def get_personal_bests_by_type(activity_type: str, db: Session = Depends(get_db)):
    """
    Get personal bests for a specific activity type.

    - **activity_type**: Must be one of: swimming, cycling, running
    """
    if activity_type.lower() not in VALID_ACTIVITY_TYPES:
        raise InvalidActivityTypeError(
            f"Invalid activity type '{activity_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_ACTIVITY_TYPES))}"
        )

    service = PersonalBestService(db)
    pbs = service.get_personal_bests_by_type(activity_type)
    return {
        "success": True,
        "data": pbs,
        "count": len(pbs)
    }
