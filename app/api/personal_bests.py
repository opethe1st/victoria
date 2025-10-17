from fastapi import APIRouter, HTTPException
from typing import List
from app.models import PersonalBestResponse
from app.database import PersonalBest

router = APIRouter()


@router.get("/personal-bests", response_model=dict)
async def get_all_personal_bests():
    """
    Get all personal bests across all activity types.

    Returns personal best records for swimming, cycling, and running.
    """
    pbs = PersonalBest.get_all()
    return {
        "success": True,
        "data": pbs,
        "count": len(pbs)
    }


@router.get("/personal-bests/{activity_type}", response_model=dict)
async def get_personal_bests_by_type(activity_type: str):
    """
    Get personal bests for a specific activity type.

    - **activity_type**: Must be one of: swimming, cycling, running
    """
    valid_types = ['swimming', 'cycling', 'running']
    if activity_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid activity type. Must be one of: {', '.join(valid_types)}"
        )

    pbs = PersonalBest.get_by_type(activity_type)
    return {
        "success": True,
        "data": pbs,
        "count": len(pbs)
    }
