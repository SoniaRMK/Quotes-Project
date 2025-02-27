import os
from dotenv import load_dotenv
from flask import Flask
from src.models import db
from src.routes import routes
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

def create_app(config=None):
    app = Flask(__name__, static_folder='static')

    # Load SECRET_KEY from environment variables or fallback
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key_here")

    # Load and fix DATABASE_URL if needed
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://")
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        raise ValueError("DATABASE_URL is not set. Check your environment variables.")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False  
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # Allow configuration overrides (e.g., for testing)
    if config:
        app.config.update(config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    CSRFProtect(app)
    Session(app)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}}, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(routes)

    return app
