from datetime import datetime
from wtforms import StringField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, NumberRange


class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(validators=[InputRequired(), NumberRange(min=1000000000, max=99999999999)])
    name = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    comment = StringField()


def check_dates(dates_list) -> bool:
    start_date = datetime.strptime(dates_list[0], '%d.%m.%Y')
    end_date = datetime.strptime(dates_list[1], '%d.%m.%Y')

    return True if (end_date - start_date).days >= 0 > (end_date - datetime.now()).days else False

