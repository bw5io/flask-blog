from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^(?=.*\d).{6,8}$', message="Your password should be between 6 and 8 characters long.")])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('Password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    mobile_phone = StringField('Mobile Phone')
    submit=SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError('Username already exist. Please choose a different one.')

def validate_email(self, email):
    email = User.query.filter_by(email=email.data).first()
    if email:
        raise ValidationError('Email already in use. Please choose a different one.')