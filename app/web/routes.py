from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime
from app.database import Activity, PersonalBest, GPSPoint
from app.config import Config
from app.fit_parser import parse_fit_file
from app.utils import calculate_pace_or_speed, format_duration, format_distance

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_template_context(request: Request, **kwargs):
    """Helper to add common context to all templates."""
    context = {
        "request": request,
        "app_name": Config.APP_NAME,
        "calculate_pace_or_speed": calculate_pace_or_speed,
        "format_duration": format_duration,
        "format_distance": format_distance
    }
    context.update(kwargs)
    return context


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Dashboard/Home page."""
    recent_activities = Activity.get_all()[:10]
    personal_bests = PersonalBest.get_all()[:5]

    return templates.TemplateResponse(
        "index.html",
        get_template_context(
            request,
            recent_activities=recent_activities,
            personal_bests=personal_bests
        )
    )


@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """File upload page."""
    return templates.TemplateResponse("upload.html", get_template_context(request))


@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    """Handle file upload and parse .fit file."""
    if not file.filename.endswith('.fit'):
        # Return to upload page with error
        return templates.TemplateResponse(
            "upload.html",
            get_template_context(request, error="Only .fit files are supported")
        )

    # Save file
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Parse the .fit file
    activity_data = parse_fit_file(filepath)

    if not activity_data:
        return templates.TemplateResponse(
            "upload.html",
            get_template_context(request, error="Failed to parse .fit file. Please ensure it's a valid file.")
        )

    # Create activity record in database
    activity_id = Activity.create(
        activity_type=activity_data['activity_type'],
        activity_date=activity_data['activity_date'],
        duration=activity_data['duration'],
        total_distance=activity_data['total_distance'],
        file_path=filepath,
        avg_heart_rate=activity_data['avg_heart_rate']
    )

    # Store GPS points if available
    if activity_data['gps_points']:
        GPSPoint.create_batch(activity_id, activity_data['gps_points'])

    # Redirect to activities page with success
    return RedirectResponse(url="/activities", status_code=303)


@router.get("/activities", response_class=HTMLResponse)
async def activities(request: Request):
    """Activities list page."""
    all_activities = Activity.get_all()
    return templates.TemplateResponse(
        "activities.html",
        get_template_context(request, activities=all_activities)
    )


@router.get("/activities/{activity_id}", response_class=HTMLResponse)
async def activity_detail(request: Request, activity_id: int):
    """Individual activity detail page."""
    activity = Activity.get_by_id(activity_id)
    if not activity:
        return RedirectResponse(url="/activities", status_code=303)

    return templates.TemplateResponse(
        "activity_detail.html",
        get_template_context(request, activity=activity)
    )


@router.get("/personal-bests", response_class=HTMLResponse)
async def personal_bests(request: Request):
    """Personal bests page."""
    swimming_pbs = PersonalBest.get_by_type('swimming')
    cycling_pbs = PersonalBest.get_by_type('cycling')
    running_pbs = PersonalBest.get_by_type('running')

    return templates.TemplateResponse(
        "personal_bests.html",
        get_template_context(
            request,
            swimming_pbs=swimming_pbs,
            cycling_pbs=cycling_pbs,
            running_pbs=running_pbs
        )
    )


@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    """Analytics and trends page."""
    return templates.TemplateResponse("analytics.html", get_template_context(request))
