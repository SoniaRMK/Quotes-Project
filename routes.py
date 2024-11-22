from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User, Quote, Vote, Report, Category  
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from services import get_quote_of_the_day, get_categorized_quotes, get_uncategorized_quotes, fetch_multiple_quotes_from_api  # Updated import
from forms import QuoteForm, SignupForm  
from flask_sqlalchemy import Pagination

logger = logging.getLogger(__name__)

routes = Blueprint('routes', __name__)

@routes.route('/')
@cross_origin()
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        # Fetch personalized quotes based on user's preferred categories
        personalized_quotes = Quote.query.join(Quote.categories).filter(Category.id.in_([c.id for c in user.categories])).all()
    else:
        personalized_quotes = []

    categorized_quotes = get_categorized_quotes()
    uncategorized_quotes = get_uncategorized_quotes()
    logger.debug("Home route accessed.")
    logger.debug(f"Categorized Quotes Retrieved: {categorized_quotes}")
    logger.debug(f"Uncategorized Quotes Retrieved: {uncategorized_quotes}")
    logger.debug(f"Personalized Quotes Retrieved: {personalized_quotes}")

    featured_qod = get_quote_of_the_day()
    community_qod = Quote.query.filter_by(is_community_qod=True).first()

    logger.info("Rendering home page with featured, community, and personalized quotes")
    return render_template(
        'index.html', 
        categorized_quotes=categorized_quotes,
        uncategorized_quotes=uncategorized_quotes,
        community_qod=community_qod,
        featured_qod=featured_qod,
        personalized_quotes=personalized_quotes
    )

@routes.before_app_request
def debug_csrf_token():
    if request.endpoint in ['routes.signup', 'routes.new_quote']:
        logger.debug(f"CSRF Token (from cookie): {request.cookies.get('csrf_token')}")
        logger.debug(f"CSRF Token (from form): {request.form.get('csrf_token')}")

@routes.route('/signup', methods=["GET", "POST"])
@cross_origin()
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        # Log the CSRF token
        logger.debug(f"Received CSRF token: {request.form.get('csrf_token')}")

        logger.debug("Signup form submitted.")
        
        # Retrieve the email, username, and password from the form
        email = form.email.data
        username = form.username.data
        password = form.password.data

        # Validate email field is provided
        if not email:
            flash('Email is required.', 'danger')
            return redirect(url_for('routes.signup'))

        # Check if the username or email already exists
        if User.query.filter_by(username=username).first():
            logger.warning(f"Attempt to create a user with existing username: {username}")
            flash('Username already exists.', 'warning')
            return redirect(url_for('routes.signup'))
        
        if User.query.filter_by(email=email).first():
            logger.warning(f"Attempt to create a user with existing email: {email}")
            flash('Email already exists.', 'warning')
            return redirect(url_for('routes.signup'))

        # Hash the password and create a new user
        password_hash = generate_password_hash(password)
        new_user = User(email=email, username=username, password_hash=password_hash)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        logger.info(f"New user created: {username}")
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('signup.html', form=form)

@routes.route('/login', methods=["GET", "POST"])
@cross_origin()
def login():
    if request.method == "POST":
        logger.debug("Login form submitted.")
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            logger.warning(f"Login failed for username: {username}")
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('routes.login'))

        session['user_id'] = user.id
        logger.info(f"User {username} logged in")
        flash('Login successful!', 'success')
        return redirect(url_for('routes.home'))

    return render_template('login.html')

@routes.route('/logout')
@cross_origin()
def logout():
    user_id = session.pop('user_id', None)
    logger.info(f"User {user_id} logged out")
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.home'))

@routes.route('/quotes', methods=["GET"])
@cross_origin()
def view_quotes():
    logger.debug("View quotes page accessed.")

    # Search functionality remains the same if applicable
    search_query = request.args.get('search', '')
    expanded_categories = request.args.get('expanded_categories', '').split(',')

    if search_query:
        logger.info(f"Searching for quotes with query: {search_query}")
        quotes = Quote.query.filter(
            (Quote.text.ilike(f"%{search_query}%")) |
            (Quote.author.ilike(f"%{search_query}%")) |
            (User.username.ilike(f"%{search_query}%") & (User.id == Quote.submitted_by))
        ).order_by(Quote.id).all()
    else:
        # Only fetch quotes from the API if the current count is significantly low
        existing_quote_count = Quote.query.count()
        if existing_quote_count < 50:
            try:
                logger.info(f"Existing quotes count ({existing_quote_count}) is less than 50. Fetching more quotes from the API.")
                fetch_multiple_quotes_from_api(500 - existing_quote_count)
            except Exception as e:
                logger.error(f"Error fetching quotes from the API: {str(e)}. Proceeding with existing quotes.")

        # Retrieve pre-categorized quotes from the database
        quotes = Quote.query.order_by(Quote.id).all()

    # Group quotes by category from the database (not categorizing on each request)
    categorized_quotes = {}
    uncategorized_quotes = []
    for quote in quotes:
        if quote.categories:
            for category in quote.categories:
                if category.name not in categorized_quotes:
                    categorized_quotes[category.name] = []
                categorized_quotes[category.name].append(quote)
        else:
            uncategorized_quotes.append(quote)

    logger.info("Rendering view quotes page with grouped quotes by categories.")
    return render_template(
        'view_quotes.html', 
        categorized_quotes=categorized_quotes, 
        uncategorized_quotes=uncategorized_quotes, 
        search_query=search_query,
        expanded_categories=expanded_categories
    )

@routes.route('/quotes/new', methods=["GET", "POST"])
@cross_origin()
def new_quote():
    form = QuoteForm()
    form.categories.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        logger.debug("New quote form submitted.")
        
        if 'user_id' not in session:
            logger.warning("User must be logged in to submit a quote.")
            flash('You need to be logged in to submit a quote.', 'warning')
            return redirect(url_for('routes.login'))

        new_quote = Quote(text=form.text.data, author=form.author.data, submitted_by=session['user_id'])
        db.session.add(new_quote)

        # Associate categories with the quote
        if form.categories.data:
            selected_categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
            new_quote.categories.extend(selected_categories)

        db.session.commit()

        logger.info("New quote submitted successfully.")
        flash('Quote submitted successfully!', 'success')
        return redirect(url_for('routes.view_quotes'))

    logger.debug("Rendering new quote form.")
    return render_template('submit_quote.html', form=form)

@routes.route('/preferences', methods=["GET", "POST"])
@cross_origin()
def preferences():
    if 'user_id' not in session:
        logger.warning("Attempt to access preferences without logging in.")
        flash('You need to be logged in to set preferences.', 'warning')
        return redirect(url_for('routes.login'))

    user = User.query.get(session['user_id'])
    categories = Category.query.all()

    if not categories:
        logger.debug("No categories available, rendering an empty form.")
        return render_template('preferences.html', user=user, categories=categories)

    if request.method == "POST":
        logger.debug("Preferences form submitted.")
        selected_category_ids = request.form.getlist('categories')
        selected_categories = Category.query.filter(Category.id.in_(selected_category_ids)).all()

        user.categories = selected_categories
        db.session.commit()

        logger.info("User preferences updated.")
        flash('Your preferences have been updated.', 'success')
        return redirect(url_for('routes.home'))

    logger.debug("Rendering preferences form.")
    return render_template('preferences.html', user=user, categories=categories)

@routes.route('/vote/<int:quote_id>', methods=["POST"])
@cross_origin()
def vote_quote(quote_id):
    logger.debug(f"Vote request received for quote ID {quote_id}")
    if 'user_id' not in session:
        logger.warning("User must be logged in to vote.")
        flash('You need to be logged in to vote.', 'danger')
        return redirect(url_for('routes.login'))

    try:
        user_id = session['user_id']
        vote_type = request.form.get('vote_type')

        if not vote_type:
            logger.error("Invalid vote type provided.")
            flash('Invalid vote type.', 'danger')
            return redirect(request.referrer or url_for('routes.home'))

        quote = Quote.query.get_or_404(quote_id)
        logger.info(f"Updating vote for quote ID {quote_id}")

        existing_vote = Vote.query.filter_by(user_id=user_id, quote_id=quote_id).first()

        if not existing_vote:
            logger.debug(f"Creating new Vote: User ID {user_id}, Quote ID {quote_id}, Vote Type {vote_type}")
            new_vote = Vote(user_id=user_id, quote_id=quote_id, vote_type=vote_type)
            db.session.add(new_vote)

            if vote_type == 'upvote':
                quote.upvotes += 1
            elif vote_type == 'downvote':
                quote.downvotes += 1
            flash('Vote added successfully!', 'success')

        else:
            if existing_vote.vote_type == vote_type:
                # User clicked the same vote type, remove the vote
                logger.info(f"User {user_id} clicked the same vote type. Removing vote for quote ID {quote_id}.")
                if vote_type == 'upvote':
                    quote.upvotes -= 1
                elif vote_type == 'downvote':
                    quote.downvotes -= 1
                db.session.delete(existing_vote)
                flash('Vote removed successfully.', 'info')

            else:
                # User changed vote type
                logger.info(f"User {user_id} already voted on quote ID {quote_id}. Updating vote.")
                if existing_vote.vote_type == 'upvote':
                    quote.upvotes -= 1
                elif existing_vote.vote_type == 'downvote':
                    quote.downvotes -= 1

                # Update vote type
                existing_vote.vote_type = vote_type

                # Adjust counts
                if vote_type == 'upvote':
                    quote.upvotes += 1
                elif vote_type == 'downvote':
                    quote.downvotes += 1
                flash('Vote updated successfully!', 'success')

        # Commit changes to the database
        db.session.commit()
        logger.info(f"Vote successfully updated for quote ID {quote_id}")

        # Redirect to the previous page or specified next page
        next_page = request.args.get('next') or request.referrer or url_for('routes.home')
        expanded = request.args.get('expanded', '')
        if expanded:
            next_page += f"&expanded={expanded}"

        return redirect(next_page)

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error occurred during voting process: {str(e)}")
        flash('An error occurred while processing your vote. Please try again.', 'danger')
        return redirect(request.referrer or url_for('routes.home'))
