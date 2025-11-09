import os

class Config:
    """Application configuration."""

    # Application name
    APP_NAME = os.environ.get('APP_NAME', 'IweKekeSare')

    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Debug mode
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

    # Database configuration
    DATABASE_URL = os.environ.get(
        'DATABASE_URL',
        'postgresql://victoria:victoria@localhost:5432/victoria'
    )

    # Upload configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
