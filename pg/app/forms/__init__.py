"""Signup & login forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

from app.core import IMAGES


class SignupForm(FlaskForm):
    """User Signup Form."""
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[Length(min=6),
                                    Email(message='Enter a valid email.'),
                                    DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    website = StringField('Website', validators=[Optional()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class UploadImageForm(FlaskForm):
    animal_image = FileField('Animal Image', validators=[FileRequired(), FileAllowed(IMAGES, 'Images only!')])
