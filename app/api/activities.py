from fastapi import APIRouter, HTTPException
from typing import List
from app.models import ActivityResponse
from app.database import Activity

router = APIRouter()


@router.get("/activities", response_model=dict)
async def get_activities():
    """
    Get all activities.

    Returns a list of all fitness activities in the database.
    """
    activities = Activity.get_all()
    return {
        "success": True,
        "data": activities,
        "count": len(activities)
    }


@router.get("/activities/{activity_id}", response_model=dict)
async def get_activity(activity_id: int):
    """
    Get a specific activity by ID.

    - **activity_id**: The ID of the activity to retrieve
    """
    activity = Activity.get_by_id(activity_id)
    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    return {
        "success": True,
        "data": activity
    }
