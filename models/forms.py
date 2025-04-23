from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class CreateEventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    event_date = DateField('Date', validators=[DataRequired()])
    event_location = StringField('Location', validators=[DataRequired()])
    event_description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Event')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters."),
    ])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[
        Optional(),
        Length(min=8, message="Password must be at least 8 characters.")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        Optional(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Update Profile')