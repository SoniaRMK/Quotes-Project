Quotes App - README
Project Overview

The Quotes App is a dynamic web application that provides users with daily quotes, categorized and uncategorized collections, the ability to vote on quotes, and sharing options on social media. Built with Python, Flask, and PostgreSQL, the app also incorporates HTML, CSS, JavaScript, and Bootstrap for an engaging front-end experience. The application fetches quotes from an external API and also provides users with personalized content.

Live Deployment: Quotes App
Features

    Daily Quote: Displays a featured quote of the day and a community-voted quote of the day.
    Personalized Quotes: Provides users with quotes based on their preferences.
    Quote Categories: Allows users to view quotes sorted into categories as well as uncategorized quotes.
    Voting System: Users can upvote or downvote quotes, with votes determining the community quote of the day.
    User-Submitted Quotes: Allows users to submit their own quotes, which can then be voted on by the community.
    Search Functionality: Users can search for quotes, authors, and users.
    Social Media Sharing: Users can share quotes on Twitter and Facebook.
    Pagination: Quotes are displayed across multiple pages, each with a consistent number of categories for easy browsing.

Technologies Used

    Backend: Python, Flask, SQLAlchemy, PostgreSQL
    Frontend: HTML, CSS, Bootstrap, JavaScript, Jinja
    Other: RESTful APIs, WTForms, JavaScript (including AJAX)
    Deployment: Render

Challenges and Lessons Learned

    JavaScript and AJAX Implementation: Initially, we planned to use JavaScript and AJAX to handle certain functionalities, such as voting on quotes without requiring a page reload. Despite multiple implementation attempts, the JavaScript code initially did not execute in the browser. This issue persisted despite various troubleshooting efforts, including verifying static file paths, adjusting script tags, and exploring potential CORS issues.

    Eventually, we opted for a combination of server-side handling via Flask forms, followed by page redirection to preserve the desired functionality. This ensured a smooth experience for users, even if it required full page reloads. Later, we revisited JavaScript and managed to successfully incorporate AJAX for more interactive user experiences in certain areas.

    This experience taught us the importance of adaptability when facing unexpected technical challenges. It also highlighted the value of simplifying the approach when necessary and consistently testing and debugging to achieve a stable user experience.

    Deployment Challenges: Deploying the Quotes App involved overcoming multiple challenges with cloud platforms and database migrations. We faced issues regarding PostgreSQL setup, Alembic migration conflicts, and deployment configurations for platforms such as Heroku and Render. This journey helped us learn about resolving dependency issues, configuring environment variables, and optimizing the deployment workflow.

How to Run the Project

Clone the repository:

git clone https://github.com/hatchways-community/capstone-project-one-a9d2b2b2324640f1bd07f85d7da2cb12.git


Set up the virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Set up the PostgreSQL database:

    Create a PostgreSQL database named quotes_app.
    Update the .env file with your database credentials.

Run the Flask application:

flask run

Access the Quotes App:

    Open your browser and navigate to http://127.0.0.1:5000 to start using the Quotes App.

Future Improvements

    Enhanced User Authentication: Add more robust user authentication and security features.
    Better Highlighting of Top Quotes: Implement a system to better highlight highly-rated quotes, ensuring the best quotes are easily visible to all users.
    Refined User Preferences on Home Page: Improve how user-preferred quotes are displayed on the home page for a more personalized experience.
    Improved Mobile Design: Further refine the user interface to enhance responsiveness and user experience on mobile devices.
    Refined Pagination: Improve pagination to ensure consistent and intuitive navigation across all quote categories.

Feel free to test out the live version of the application and let us know if you encounter any issues or have suggestions for further improvements.
