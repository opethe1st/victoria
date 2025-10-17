# Docker Setup Guide

This application can be run entirely with Docker and Docker Compose, using PostgreSQL as the database.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Quick Start

Start the entire application stack with a single command:

```bash
docker-compose up
```

Or run in detached mode:

```bash
docker-compose up -d
```

## What Gets Started

The `docker-compose up` command starts two services:

1. **PostgreSQL Database** (`victoria-db`)
   - PostgreSQL 16 (Alpine Linux)
   - Accessible on `localhost:5432`
   - Database: `victoria`
   - Username: `victoria`
   - Password: `victoria`
   - Data persisted in Docker volume

2. **FastAPI Web Application** (`victoria-web`)
   - Built from local Dockerfile
   - Accessible on `http://localhost:8000`
   - API Documentation: `http://localhost:8000/api/docs`
   - Auto-reloads on code changes (development mode)

## Accessing the Application

Once running:

- **Web Interface:** http://localhost:8000
- **API Documentation (Swagger):** http://localhost:8000/api/docs
- **API Documentation (ReDoc):** http://localhost:8000/api/redoc
- **Database:** localhost:5432

## Common Commands

### Start services
```bash
docker-compose up
```

### Start in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes (deletes database data)
```bash
docker-compose down -v
```

### View logs
```bash
docker-compose logs -f
```

### View specific service logs
```bash
docker-compose logs -f web
docker-compose logs -f db
```

### Rebuild containers
```bash
docker-compose up --build
```

### Access database directly
```bash
docker-compose exec db psql -U victoria -d victoria
```

### Access web container shell
```bash
docker-compose exec web sh
```

## Environment Variables

You can customize the application by setting environment variables in `docker-compose.yml`:

- `DATABASE_URL`: PostgreSQL connection string
- `APP_NAME`: Application name (default: IweKekeSare)
- `SECRET_KEY`: Application secret key

## Development Workflow

1. **Start the services:**
   ```bash
   docker-compose up
   ```

2. **Make code changes** - the web service will auto-reload

3. **View logs** in the terminal running docker-compose

4. **Stop when done:**
   ```bash
   Ctrl+C  # or docker-compose down in another terminal
   ```

## Database Migrations

The application automatically creates database tables on startup. If you need to reset the database:

```bash
# Stop services and remove volumes
docker-compose down -v

# Start fresh
docker-compose up
```

## Troubleshooting

### Port already in use
If port 8000 or 5432 is already in use, you can change it in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change host port
```

### Database connection issues
The web service waits for the database to be healthy before starting. If you see connection errors, the database might need more time. The health check ensures PostgreSQL is ready.

### Container won't start
Check logs:
```bash
docker-compose logs
```

Rebuild images:
```bash
docker-compose up --build
```

## Production Deployment

For production:

1. Change database credentials in `docker-compose.yml`
2. Set a strong `SECRET_KEY` environment variable
3. Consider using environment files (`.env`)
4. Use a proper reverse proxy (nginx, traefik)
5. Enable HTTPS
6. Set up proper database backups

## File Uploads

Uploaded `.fit` files are stored in the `./uploads` directory, which is mounted as a volume. This ensures files persist even if containers are recreated.
