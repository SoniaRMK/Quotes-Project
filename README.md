# Quotes App

## Project Overview
The **Quotes App** provides users with daily quotes, voting features, and social media sharing. Built with **Python**, **Flask**, and **PostgreSQL**, it supports personalized and categorized quotes.

Live version: [Quotes App](https://quotes-project-fmxp.onrender.com)

## Features
- **Daily Quotes:** Featured & community-voted quotes.
- **Personalized Quotes:** Based on user preferences.
- **Voting System:** Upvote/Downvote quotes.
- **Search Functionality:** Search quotes by text, author, or user.
- **Social Media Sharing:** Easily share quotes on Twitter and Facebook.
- **Pagination:** Browse quotes across multiple pages.

## Technologies Used
- **Backend:** Python, Flask, SQLAlchemy, PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Other:** RESTful APIs, WTForms, Flask-WTF, AJAX, Render Deployment

## How to Run the Project

### 1️⃣ Clone the Repository:
```bash
git clone https://github.com/hatchways-community/capstone-project-one.git
cd capstone-project-one

2️⃣ Install Dependencies:
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
pip install -r requirements.txt

3️⃣ Setup Environment:
Copy .env.example .env
Fill in DATABASE_URL, SECRET_KEY, API_TOKEN.

4️⃣ Initialize the Database:
flask db upgrade

5️⃣ Run the Application:
flask run

6️⃣ Run Tests:
pytest
