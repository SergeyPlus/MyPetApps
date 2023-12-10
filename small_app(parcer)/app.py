from flask import Flask, request
from werkzeug.exceptions import InternalServerError
from checking import check_dates
from parcing_code import get_dict_with_data
from registration import RegistrationForm

app = Flask(__name__)


@app.route('/find_price/', methods=['GET'])
def find_price() -> str:
    """ The function recieves GET request - start_date and end_date. Based on this period it
    calls parcing_code module in order to get from CB RF web-site pricing information. Before the calling
    received dates checking by module checking"""
    req_dates = request.args.getlist('date', type=str)
    if check_dates(req_dates):
        result = get_dict_with_data(req_dates[0], req_dates[1])
        if result:
            return '<h3>Данные по металлам за период с {} по {}:</h3> {}'.format(
                req_dates[0], req_dates[1], result)
        return '<h2>В запрошенный диапазон дат цены на металлы не обнаружены. Измените диапазон</h2>'


@app.route('/registration', methods=['POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        phone = form.phone.data
        email = form.email.data

        return '<h3>***ФОРМА РЕГИСТРАЦИИ***</h3>\n' \
               'Имя: {}\n' \
               'Фамилия: {}\n' \
               'Телефон: {}\n' \
               'Эл. почта: {}'.format(name, surname, phone, email)
    error_list = form.errors
    return '<h3>***ОШИБКА***</h3>\n' \
           'проверьте корректность ввода полей: \n' \
           '{}'.format(error_list)


@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError):
    original = getattr(e, 'original_exception', None)

    if isinstance(original, ValueError):
        with open('Invalid_error.log', 'a') as fo:
            fo.write(
                f'Error decryption: {e.description}. Exception info: {original}\n')
    return f'<h2>Internal server error</h2>' \
           f'<h5>Please specify date properly in accordance with:</h5>' \
           f'   <h5>- the date format is dd.mm.yyyy,</h5>' \
           f'   <h5>- first date should be earlier than second date</h5>'


if __name__ == "__main__":
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)




