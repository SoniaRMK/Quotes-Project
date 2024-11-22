from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email

class QuoteForm(FlaskForm):
    text = StringField('Quote Text', validators=[DataRequired()])
    author = StringField('Author', default='Unknown')
    categories = SelectMultipleField('Categories', coerce=int)
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
