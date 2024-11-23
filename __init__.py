from dotenv import load_dotenv
from flask import Flask
from quotes_app.models import db  
from quotes_app.routes import routes  
from flask_migrate import Migrate
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration from environment or default
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key_here")

# Update DATABASE_URL to use 'postgresql' dialect if needed
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
Session(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(routes)
