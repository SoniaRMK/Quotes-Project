import os
from dotenv import load_dotenv
from flask import Flask, send_from_directory, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import logging
from models import db
from routes import routes
from tasks import scheduler
from services import fetch_multiple_quotes_from_api

# Load environment variables
load_dotenv()

# Set up Flask app
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key_here")

# Configurations
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Configure session storage to enable CSRF tokens
app.config['SESSION_PERMANENT'] = False  # Use non-permanent sessions
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Adds extra security to session cookie


# Initialize session handling
Session(app)

# Initialize CSRF protection
csrf = CSRFProtect()
csrf.init_app(app)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}}, supports_credentials=True)

# Register Blueprints
app.register_blueprint(routes)


# Start the scheduler if it is not already running (handled in `tasks.py`)
if not scheduler.running:
    scheduler.start()
    logger.info("Background scheduler started.")

@app.route('/fetch-quotes', methods=['GET'])
def fetch_quotes():
    try:
        quotes_fetched = fetch_multiple_quotes_from_api()  # Call the function that fetches quotes
        return jsonify({"status": "success", "message": "Quotes fetched successfully", "quotes_fetched": quotes_fetched}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Serve static files manually if Flask fails to serve them
@app.route('/static/<path:filename>')
def custom_static(filename):
    logger.debug(f"Serving static file: {filename}")
    return send_from_directory(app.static_folder, filename)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
