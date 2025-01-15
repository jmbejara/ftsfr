from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config  # Import the config dictionary
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    app = Flask(__name__)

    # Determine the configuration to use
    if config_name is None:
        config_name = os.getenv("FLASK_ENV") or "default"

    # Use the configuration class from the config dictionary
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register Blueprints
    from .routes import main

    app.register_blueprint(main)

    with app.app_context():
        from . import models

    return app
