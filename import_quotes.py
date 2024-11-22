import json
import os
from models import db, Quote, Category
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a Flask app instance
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your_secret_key_here")

# Initialize extensions
db.init_app(app)

# Create a Flask app context so we can interact with the database
with app.app_context():
    # Open the JSON file and load quotes
    with open('bulk_quotes.json', 'r') as file:
        quotes_data = json.load(file)

    # Iterate through the quotes and add them to the database
    for item in quotes_data.get('quotes', []):
        # Extract the necessary information from each quote
        text = item.get('text')
        author = item.get('author', 'Unknown')  # Default to 'Unknown' if no author is provided
        category_name = item.get('category', 'Uncategorized')  # Default to 'Uncategorized' if no category

        # Find or create the category
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()  # Commit after adding a new category

        # Check if the quote already exists to avoid duplicates
        existing_quote = Quote.query.filter_by(text=text).first()
        if not existing_quote:
            # Create a new quote and associate it with the category
            new_quote = Quote(text=text, author=author)
            new_quote.categories.append(category)

            # Add the quote to the session
            db.session.add(new_quote)

    # Commit the session to save quotes to the database
    db.session.commit()

    print("Quotes imported successfully!")
