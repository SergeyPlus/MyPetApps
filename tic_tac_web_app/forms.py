from typing import List
from flask_wtf import Form, FlaskForm
from wtforms import StringField, EmailField, TelField, PasswordField, IntegerField
from wtforms.validators import InputRequired, ValidationError, Email, Length, NumberRange, EqualTo
import re


class MyRegistrationForm(FlaskForm):
    """
    The class serves checks registration form
    All input required conditions makes in HTML input tag
    phone length and consistent checks in HTML input tag
    """
    name = StringField('name',validators=[
                       Length(max=120, message='too much long name, please check it')])
    phone = IntegerField('phone')
    email = EmailField('email',
                        validators=[
                            Email(message='that\'s not a valid email address, please check it'),
                            Length(min=6, max=120, message='that\'s not a valid email address, please check it')])
    login = StringField('login')
    password = PasswordField('password',
                        validators=[
                            Length(min=8, max=120),
                            EqualTo('confirm', message='password 1 and password 2 should be equal')])
    confirm = PasswordField('pass2')

    def validate_password(form, field):
        """
        Passwords should content special symbols - /!@#$%^&*
        Password should content of 1 capitalize symbol
        """
        pattern = r'[/!@#$%^&*]'
        result: List = re.findall(pattern, field.data)
        if len(result) < 2:
            raise ValidationError('password should content of minimum 2 spec symbols /!@#$%^&*')
        pattern = r'[A-Z]'
        result: List = re.findall(pattern, field.data)
        if not len(result):
            raise ValidationError('password should content of minimum 1 capitalize')


class MyLogInForm(FlaskForm):
    """
    The class serves checks form for log in
    All input required conditions makes in HTML input tag

    """
    login = StringField('login')
    password = StringField('password')


class PlayersForms(FlaskForm):
    """
    The class serves checks form for inputting player name during tic tac game
    All input required conditions makes in HTML input tag
    """
    player_1_name = StringField('player_1_name')
    player_2_name = StringField('player_2_name')


class TicTacFieldTable(FlaskForm):
    """
    The class serves checks form for tic tac game
    All input required conditions makes in HTML input tag
    phone length and consistent checks in HTML input tag
    """
    nod_0 = StringField('nod_0')
    nod_1 = StringField('nod_0')
    nod_2 = StringField('nod_0')
    nod_3 = StringField('nod_0')
    nod_4 = StringField('nod_0')
    nod_5 = StringField('nod_0')
    nod_6 = StringField('nod_0')
    nod_7 = StringField('nod_0')
    nod_8 = StringField('nod_0')


if __name__ == '__main__':
    pass
