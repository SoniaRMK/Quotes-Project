import os

class Config:
    """Base configuration class"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30
    }
    DEBUG = False

class DevelopmentConfig(Config):
    """Configuration for development"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    DEBUG = True

class ProductionConfig(Config):
    """Configuration for production"""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///prod.db")
    DEBUG = False
