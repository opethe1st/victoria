from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
from datetime import datetime
from app.database import get_db
from app.services import ActivityService, PersonalBestService
from app.config import Config
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
async def index(request: Request, db: Session = Depends(get_db)):
    """Dashboard/Home page."""
    activity_service = ActivityService(db)
    pb_service = PersonalBestService(db)

    recent_activities = activity_service.get_all_activities()[:10]
    personal_bests = pb_service.get_all_personal_bests()[:5]

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
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
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

    # Use service layer to create activity from FIT file
    activity_service = ActivityService(db)
    activity_id = activity_service.create_from_fit_file(filepath)

    if not activity_id:
        return templates.TemplateResponse(
            "upload.html",
            get_template_context(request, error="Failed to parse .fit file. Please ensure it's a valid file.")
        )

    # Redirect to activities page with success
    return RedirectResponse(url="/activities", status_code=303)


@router.get("/activities", response_class=HTMLResponse)
async def activities(request: Request, db: Session = Depends(get_db)):
    """Activities list page."""
    activity_service = ActivityService(db)
    all_activities = activity_service.get_all_activities()
    return templates.TemplateResponse(
        "activities.html",
        get_template_context(request, activities=all_activities)
    )


@router.get("/activities/{activity_id}", response_class=HTMLResponse)
async def activity_detail(request: Request, activity_id: int, db: Session = Depends(get_db)):
    """Individual activity detail page."""
    activity_service = ActivityService(db)
    activity = activity_service.get_activity_by_id(activity_id)
    if not activity:
        return RedirectResponse(url="/activities", status_code=303)

    return templates.TemplateResponse(
        "activity_detail.html",
        get_template_context(request, activity=activity)
    )


@router.get("/personal-bests", response_class=HTMLResponse)
async def personal_bests(request: Request, db: Session = Depends(get_db)):
    """Personal bests page."""
    pb_service = PersonalBestService(db)
    swimming_pbs = pb_service.get_personal_bests_by_type('swimming')
    cycling_pbs = pb_service.get_personal_bests_by_type('cycling')
    running_pbs = pb_service.get_personal_bests_by_type('running')

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
