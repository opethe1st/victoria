# Victoria - Fitness Activity Tracker

A web application for tracking and analyzing fitness activities (swimming, cycling, running) with personal best tracking and analytics.

## Project Structure

```
victoria/
├── app/
│   ├── api/                # API endpoints (REST API)
│   │   ├── __init__.py
│   │   ├── activities.py   # Activity API endpoints
│   │   └── personal_bests.py # Personal bests API endpoints
│   ├── web/                # Web routes (HTML pages)
│   │   ├── __init__.py
│   │   └── routes.py       # Web page routes
│   ├── templates/          # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── activities.html
│   │   ├── activity_detail.html
│   │   ├── personal_bests.html
│   │   └── analytics.html
│   ├── static/             # CSS, JS, images
│   │   ├── css/
│   │   └── js/
│   ├── app.py             # Flask application factory
│   ├── config.py          # Application configuration
│   └── database.py        # Database models and queries
├── data/                  # SQLite database storage
├── uploads/               # Uploaded .fit files
├── requirements.txt       # Python dependencies
├── claude.md             # Project specification
├── API.md                # API documentation
└── README.md             # This file
```

## Quick Start with Docker (Recommended)

The easiest way to run the application is with Docker:

```bash
docker-compose up
```

That's it! The application and PostgreSQL database will start automatically.

Access the application:
- **Web Interface:** `http://localhost:8000`
- **API Documentation (Swagger):** `http://localhost:8000/api/docs`
- **API Documentation (ReDoc):** `http://localhost:8000/api/redoc`

See [DOCKER.md](DOCKER.md) for detailed Docker documentation.

## Manual Setup (Alternative)

If you prefer to run without Docker:

1. **Install PostgreSQL** and create a database named `victoria`

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set database URL:**
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/victoria"
   ```

5. **Run the application:**
   ```bash
   cd app
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

6. **Access the webapp:**
   - **Web Interface:** `http://127.0.0.1:8000`
   - **API Documentation (Swagger):** `http://127.0.0.1:8000/api/docs`
   - **API Documentation (ReDoc):** `http://127.0.0.1:8000/api/redoc`
   - **OpenAPI JSON:** `http://127.0.0.1:8000/api/openapi.json`

## Current Status

### Completed (Skeleton)
- ✅ Project structure
- ✅ Database schema and models
- ✅ Flask app with routing
- ✅ All page templates with basic UI
- ✅ Navigation and layout

### Not Yet Implemented
- ⏳ .fit file parsing and processing
- ⏳ Personal best calculation algorithm
- ⏳ Analytics and time aggregation
- ⏳ Charts and visualizations
- ⏳ GPS data processing and map display

## Next Steps

See `claude.md` for the full specification and implementation phases. The next feature to implement would be:

1. **Phase 2: Activity Management** - .fit file parsing and storage
2. **Phase 3: Personal Bests** - PB calculation algorithm
3. **Phase 4: Analytics** - Time tracking and visualization

## Technology Stack

- **Backend:** FastAPI (Python) with automatic OpenAPI documentation
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Frontend:** HTML, Tailwind CSS, Chart.js
- **API:** RESTful API (v1) at `/api/v1` with Swagger UI and ReDoc
- **File Processing:** fitparse (for .fit files)
- **Server:** Uvicorn ASGI server
- **Deployment:** Docker & Docker Compose

## Architecture

The application follows a modular router architecture with FastAPI:

- **Web Routes** (`/`) - Traditional web interface for browser access
- **API Routes** (`/api/v1`) - REST API for programmatic access
- **Automatic Documentation** - OpenAPI/Swagger docs automatically generated
- **Async Support** - Built on ASGI for high performance async operations

### API Access

The application includes a full REST API with **automatic OpenAPI documentation**.

**Documentation URLs:**
- **Swagger UI (Interactive):** `http://127.0.0.1:5000/api/docs`
- **ReDoc (Alternative):** `http://127.0.0.1:5000/api/redoc`
- **OpenAPI JSON:** `http://127.0.0.1:5000/api/openapi.json`

**API Base URL:** `http://127.0.0.1:5000/api/v1`

**Example API calls:**
```bash
# Health check
curl http://127.0.0.1:5000/api/health

# Get all activities
curl http://127.0.0.1:5000/api/v1/activities

# Get running personal bests
curl http://127.0.0.1:5000/api/v1/personal-bests/running
```

The interactive Swagger UI allows you to test all API endpoints directly from your browser!

## Configuration

The app name and other settings can be configured via environment variables or by editing `app/config.py`:

```bash
# Set custom app name
export APP_NAME="MyFitnessApp"

# Set custom secret key
export SECRET_KEY="your-secret-key"
```
