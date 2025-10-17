from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app.database import init_db
from app.config import Config

# Initialize FastAPI app
app = FastAPI(
    title=Config.APP_NAME,
    description="Fitness Activity Tracker - Track your swimming, cycling, and running activities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Setup static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Ensure required directories exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Initialize database
init_db()

# Register routers
from app.api import activities as api_activities
from app.api import personal_bests as api_personal_bests
from app.web import routes as web_routes

app.include_router(api_activities.router, prefix="/api/v1", tags=["activities"])
app.include_router(api_personal_bests.router, prefix="/api/v1", tags=["personal-bests"])
app.include_router(web_routes.router, tags=["web"])

# Make config available to templates
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app_name": Config.APP_NAME}
