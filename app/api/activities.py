from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models import ActivityResponse
from app.database import get_db
from app.services import ActivityService

router = APIRouter()


@router.get("/activities", response_model=dict)
async def get_activities(db: Session = Depends(get_db)):
    """
    Get all activities.

    Returns a list of all fitness activities in the database.
    """
    service = ActivityService(db)
    activities = service.get_all_activities()
    return {
        "success": True,
        "data": activities,
        "count": len(activities)
    }


@router.get("/activities/{activity_id}", response_model=dict)
async def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Get a specific activity by ID.

    - **activity_id**: The ID of the activity to retrieve
    """
    service = ActivityService(db)
    activity = service.get_activity_by_id(activity_id)
    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activity not found"
        )

    return {
        "success": True,
        "data": activity
    }
