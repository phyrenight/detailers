from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    first_name = StringField(
        'First name',
        validators=[DataRequired('Please enter your first name')])
    last_name = StringField(
        'Last name',
        validators=[DataRequired('Please enter your last name')])
    email = StringField(
        'Email',
        validators=[DataRequired(
            'Please enter your email address'),
            Email('Please enter a valid email address')])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired('Please enter a password'),
            Length(
                min=8,
                message='Password must be at least 8 characters long')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired('Please enter your email address'),
            Email('Please enter a valid email')])
    password = PasswordField(
        'Password',
        validators=[DataRequired('Please enter your password')])
    submit = SubmitField('Sign in')


class RequestPasswordReset(FlaskForm):
    email = StringField(
        'Enter your email address',
        validators=[DataRequired('Please enter your email address')],
        render_kw={'placeholder': 'email@email.com'})
    submit = SubmitField('Submit request')


class ChangePassword(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired('Please enter your email.')],
        render_kw={'placeholder': 'email@email.com' })
    password = PasswordField

