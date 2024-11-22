Quotes App - README

Project Overview

The Quotes App is a web application that provides users with daily quotes, allows them to view categorized and uncategorized quotes, vote on quotes, and share them on social media. The application is built using Python, Flask, PostgreSQL, and other technologies such as HTML, CSS, and Bootstrap for front-end styling. The app also makes use of an external API to fetch quotes.

Features

Daily Quote: Displays a featured quote of the day and a community-voted quote of the day.

Quote Categories: View categorized quotes and uncategorized quotes.

Vote on Quotes: Users can upvote or downvote quotes.

Search Functionality: Users can search for quotes, authors, and users.

Social Media Sharing: Users can share quotes on Twitter and Facebook.

Technologies Used

Backend: Python, Flask, SQLAlchemy, PostgreSQL

Frontend: HTML, CSS, Bootstrap, Jinja

Other: RESTful APIs, WTForms

Deployment: Heroku

Challenges and Lessons Learned

JavaScript and AJAX Issue

Initially, we planned to use JavaScript and AJAX to handle certain functionalities, such as voting on quotes without requiring a page reload. However, despite multiple implementation attempts, none of the JavaScript code was being acknowledged or executed in the browser. This issue persisted even when JavaScript was directly added to the HTML files.

After extensive troubleshooting, including verifying static file paths, ensuring the script tags were properly linked, and exploring potential CORS issues, we ultimately decided to switch to using form submissions and redirect logic within Flask to handle the interactions. This approach resolved the issue and ensured the intended functionality without requiring JavaScript.

This experience emphasized the importance of adaptability and finding alternative solutions when faced with challenges. It also reinforced the significance of testing and debugging effectively, as well as the value of keeping functionality simple when facing technical limitations.

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

Open your browser and navigate to http://127.0.0.1:5000 to access the Quotes App.

Future Improvements

Improved User Authentication: Add more robust user authentication and security features.

AJAX Functionality: Revisit the JavaScript and AJAX implementation to enhance user experience by enabling smoother, asynchronous interactions.

Enhanced Quote Management: Allow users to submit their own quotes for community voting.

Better UI Design: Further improve the user interface and mobile responsiveness.

License

This project is licensed under the MIT License.