import os

class Config:
    """Application configuration."""

    # Application name
    APP_NAME = os.environ.get('APP_NAME', 'IweKekeSare')

    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Upload configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
