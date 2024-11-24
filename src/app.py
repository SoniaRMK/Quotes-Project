import os
import sys
from dotenv import load_dotenv
from src import create_app
from src.models import db
from flask_migrate import Migrate  
import logging

# Load environment variables
load_dotenv()

# Create the app instance using the factory function
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)  # Add this line to initialize Migrate with app and db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start the scheduler if it is not already running (handled in `tasks.py`)
from src.tasks import scheduler

if not scheduler.running:
    scheduler.start()
    logger.info("Background scheduler started.")

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
