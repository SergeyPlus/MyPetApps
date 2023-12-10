from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField
from wtforms.validators import InputRequired, Email, NumberRange, Length


class RegistrationForm(FlaskForm):
    name = StringField('name',
                       validators=[InputRequired(message='Please specify Your name'),
                                   Length(max=20, message='Name should be less than 20 symbols')])
    surname = StringField('surname',
                          validators=[InputRequired(message='Please specify Your surname'),
                                      Length(max=20, message='Name should be less than 20 symbols')])
    phone = IntegerField('phone',
                         validators=[InputRequired('Please specify Your name'),
                                     NumberRange(min=1000000000, max=9999999999,
                                                 message='Phone number should consist of 10 number')])
    email = EmailField('email',
                       validators=[InputRequired(message='Please specify Your email'),
                                   Email(check_deliverability=True, message='Email is not correct. Please try again')])
