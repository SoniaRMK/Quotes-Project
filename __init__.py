from flask import Flask
from models import db  
from routes import routes  
from flask_migrate import Migrate
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

# Load configuration from environment or default
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key_here")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
Session(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(routes)
