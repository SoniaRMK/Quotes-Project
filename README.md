Quotes App - README

Project Overview

The Quotes App is a dynamic web application that provides users with daily quotes, categorized and uncategorized collections, the ability to vote on quotes, and sharing options on social media. Built with Python, Flask, and PostgreSQL, the app also incorporates HTML, CSS, JavaScript, and Bootstrap for an engaging front-end experience. The application fetches quotes from an external API and also provides users with personalized content.

The live version of the app is available at: [Quotes App](https://quotes-project-fmxp.onrender.com)

Features

Daily Quote: Displays a featured quote of the day and a community-voted quote of the day.

Personalized Quotes: Provides users with quotes based on their preferences.

Quote Categories: Allows users to view quotes sorted into categories as well as uncategorized quotes.

Voting System: Users can upvote or downvote quotes, with votes determining the community quote of the day.

Search Functionality: Users can search for quotes, authors, and users.

Social Media Sharing: Users can share quotes on Twitter and Facebook.

Pagination: Quotes are displayed across multiple pages, each with a consistent number of categories for easy browsing.

Technologies Used

Backend: Python, Flask, SQLAlchemy, PostgreSQL

Frontend: HTML, CSS, Bootstrap, JavaScript, Jinja

Other: RESTful APIs, WTForms, JavaScript (including AJAX)

Deployment: Render

Challenges and Lessons Learned

JavaScript and AJAX Implementation

Initially, we planned to use JavaScript and AJAX to handle certain functionalities, such as voting on quotes without requiring a page reload. Despite multiple implementation attempts, the JavaScript code initially did not execute in the browser. This issue persisted despite various troubleshooting efforts, including verifying static file paths, adjusting script tags, and exploring potential CORS issues.

Eventually, we opted for a combination of server-side handling via Flask forms, followed by page redirection to preserve the desired functionality. This ensured a smooth experience for users, even if it required full page reloads.

Later, we revisited JavaScript and managed to successfully incorporate AJAX for a more interactive user experience. The AJAX-based features now work effectively, enhancing the responsiveness of the application.

This experience taught us the importance of adaptability when facing unexpected technical challenges. It also highlighted the value of simplifying the approach when necessary and consistently testing and debugging to achieve a stable user experience.

User Flow

Home Page: Users are greeted with the quote of the day and categorized quotes.

User Registration/Login: Users can register or log in to gain access to additional features like voting and personalized quotes.

Preferences: Users can set preferences to personalize the quotes they want to see.

Voting and Sharing: Logged-in users can vote for their favorite quotes and share them on social media.

Quote Submission: Users can submit their own quotes for others to see and vote on.

Logout: Users can log out when they are done.

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

Improved User Authentication: Add more robust user authentication and security features.

Highlight Highly Rated Quotes: Implement a more sophisticated system to prominently feature quotes with the highest community ratings, making it easier for users to see popular and impactful quotes.

Enhanced User Preferences: Reorganize the display of user preference quotes on the home page for a more personalized and user-friendly experience.

Enhanced AJAX Functionality: Expand the use of JavaScript and AJAX to make interactions smoother and more responsive.

Improved Mobile Design: Further refine the user interface to enhance responsiveness and user experience on mobile devices.

Refined Pagination: Improve pagination to ensure consistent and intuitive navigation across all quote categories.

Deployment Challenges

During the deployment to Render, several challenges were encountered, including handling database connectivity, configuring the environment, and ensuring all dependencies were correctly installed. Despite these obstacles, we were able to successfully deploy the app and resolve issues like missing tables and database migrations.

Notes on the API

The application uses the They Said So Quotes API to fetch quotes. We decided to switch to storing quotes locally to avoid API rate limits and to ensure the app functions smoothly for users without depending heavily on external API requests. Initially, we faced challenges in integrating API responses effectively, but ultimately, storing quotes in our database provided a better experience.

Feel free to test out the live version of the application and let us know if you encounter any issues or have suggestions for further improvements.