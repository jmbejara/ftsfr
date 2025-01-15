import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    # Use file-based SQLite for development
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'dev_database.db')}"


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""

    # You could use another file-based (or a real production DB).
    # For a simple setup, here’s an example of a file-based prod DB:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'prd_database.db')}"


# Dictionary to easily access configurations
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
