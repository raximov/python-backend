from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str = "development") -> Flask:
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register API blueprint
    from app.routes import register_api
    register_api(app)

    # Create all database tables
    with app.app_context():
        # Import models so they are registered with SQLAlchemy
        from app.models import address, client, supplier, product, image  # noqa: F401
        db.create_all()

    return app
