import os
from werkzeug.security import generate_password_hash
from src import create_app
from src.models import db, User

# Create the app instance
app = create_app()

# Add users to the database using the Flask app context
with app.app_context():
    try:
        users = [
            {"username": "testuser1", "email": "testuser1@example.com", "password": "password123"},
            {"username": "testuser2", "email": "testuser2@example.com", "password": "password123"},
            {"username": "testuser3", "email": "testuser3@example.com", "password": "password123"},
            {"username": "testuser4", "email": "testuser4@example.com", "password": "password123"},
        ]

        for user_data in users:
            # Generate a password hash for security
            password_hash = generate_password_hash(user_data["password"])
            
            # Create the user instance
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=password_hash,
            )
            
            # Add the user to the session
            db.session.add(user)

        # Commit the session to write the changes to the database
        db.session.commit()
        print("Users successfully added to the database.")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
