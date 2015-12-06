"""
Login and Registration web forms created using Flask-WTF extension
"""

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo
from wtforms import ValidationError
from ..model import User

class LoginForm(Form):
    """
    Login Web Form
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    """
    Registration Web Form
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    # RegExp validator used to restrict charcters that can be entered
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters '
                                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        '''
        Validates that user email address is not registered

        :param field: email address of the user
        :return: Validation error if email is already registered
        '''
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        """
        Validates if entered username is not registered

        :param field: username chosen by the user
        :return: Validation error if username is already registered
        """
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')
