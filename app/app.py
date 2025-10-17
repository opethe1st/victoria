from flask import Flask
import os
from database import init_db
from config import Config


def create_app(config_class=Config):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SECRET_KEY']

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize database
    init_db()

    # Register blueprints
    from api import api_bp
    from web import web_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    # Make config available to templates
    @app.context_processor
    def inject_config():
        return {'app_name': app.config['APP_NAME']}

    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
