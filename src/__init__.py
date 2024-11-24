from dotenv import load_dotenv
from flask import Flask
from src.models import db, User, Quote, Vote, Report, Category
from src.routes import routes  
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='static')

    # Load configuration from environment or default
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key_here")
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False  # Use non-permanent sessions
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # Initialize extensions
    db.init_app(app)  # Initialize SQLAlchemy after importing models
    csrf = CSRFProtect(app)
    Session(app)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}}, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(routes)

    return app
