from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, InputRequired
from blog.models import User
from flask import flash

class RegistrationForm(FlaskForm):
    username = StringField('Username *', validators=[DataRequired(), Length(min=3, max=15, message="Username should be 3 to 15 characters long.")],render_kw={"placeholder":"3 to 15 characters long"})
    email = StringField('Email *', validators=[DataRequired(), Email()])
    password = PasswordField('Password *', validators=[DataRequired(),Regexp('^(?=.*\d).{8,16}$',message="Your password should be between 8 and 16 characters long.")], render_kw={"placeholder":"8 to 16 characters long"})
    confirm_password=PasswordField('Confirm Password *', validators=[DataRequired(),EqualTo('password',message="Two Passwords are not the same.")])
    first_name = StringField('First Name *', validators=[DataRequired()])
    last_name = StringField('Last Name *', validators=[DataRequired()])
    mobile_phone = StringField('Mobile Phone', validators=[Regexp('^$|^[0][1-9]\d{9}$|^[1-9]\d{9}$', message="Mobile Phone number should be 10 digits long, or 11 digits long with 0 at the start.")])
    submit=SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(message='Username already exist. Please choose a different one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(message='Email already in use. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[InputRequired()], render_kw={"placeholder":"Input Comment Here."})
    submit = SubmitField('Post comment')