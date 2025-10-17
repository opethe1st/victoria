# Changelog

All notable changes to IweKekeSare (Victoria) will be documented in this file.

## [Unreleased]

### Added
- Docker and Docker Compose support for easy deployment
- PostgreSQL database with SQLAlchemy ORM
- Comprehensive Docker documentation (DOCKER.md)
- Database migrations support with Alembic
- Health check for database container
- Volume persistence for PostgreSQL data
- Auto-reload in development mode for Docker

### Changed
- Migrated from SQLite to PostgreSQL
- Updated database layer to use SQLAlchemy ORM
- Changed default port from 5000 to 8000
- Updated README with Docker-first setup instructions
- Enhanced .gitignore to exclude Docker volumes

### Maintained
- Full backward compatibility with existing API
- All existing endpoints continue to work
- Same response formats and data structures

## [0.1.0] - 2025-10-17

### Added
- Initial FastAPI application structure
- Web interface with Tailwind CSS
- Automatic OpenAPI documentation (Swagger UI and ReDoc)
- REST API v1 endpoints
- Database models for activities, GPS points, and personal bests
- File upload support for .fit files
- Configuration management with environment variables
- Complete project documentation

### Features
- Dashboard page
- Activity upload page
- Activities list page
- Personal bests tracking page
- Analytics page (placeholder)
- Health check endpoint

### Technical
- FastAPI backend with async support
- Uvicorn ASGI server
- Jinja2 templates for server-side rendering
- Pydantic models for API validation
- SQLAlchemy for database ORM
- fitparse for .fit file processing
