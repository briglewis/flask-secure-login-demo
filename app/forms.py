from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
            validators=[
            DataRequired('Please enter your email address.'), 
            Email(message='Enter a valid email address.'), 
            Length(max=254, message='Email is too long')
            ],
    )
    password = PasswordField(
        'Password', 
            validators=[
            DataRequired(message='Please enter your password.'), 
            Length(min=15, max=64, message='Password must be 15–64 characters.')
            ]
    )
            
    submit = SubmitField('Login')

"""Check if logout form has CSRF token > create an empty form class for dashboard."""
class EmptyForm(FlaskForm):
    pass