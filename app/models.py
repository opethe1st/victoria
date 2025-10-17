from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ActivityBase(BaseModel):
    activity_type: str = Field(..., description="Type of activity: swimming, cycling, or running")
    activity_date: datetime
    duration: int = Field(..., description="Duration in seconds")
    total_distance: float = Field(..., description="Total distance in meters")
    avg_heart_rate: Optional[int] = Field(None, description="Average heart rate in BPM")


class ActivityCreate(ActivityBase):
    file_path: str


class ActivityResponse(ActivityBase):
    id: int
    upload_date: datetime
    file_path: str

    class Config:
        from_attributes = True


class PersonalBestBase(BaseModel):
    activity_type: str
    distance: float = Field(..., description="Distance in meters")
    best_time: int = Field(..., description="Best time in seconds")
    avg_pace: float = Field(..., description="Average pace")
    activity_id: int
    achieved_date: datetime


class PersonalBestResponse(PersonalBestBase):
    id: int

    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    success: bool
    data: Optional[dict | List[dict]] = None
    count: Optional[int] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    app_name: str
