import logging
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


logging.basicConfig(level=10)
check_logger = logging.getLogger(__name__)


def add_data_to_database(form):
    password = generate_password_hash(form.password.data)
    check_logger.info(f'Password hash was generated{type(password)}')
    with sqlite3.connect('tic_tac.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'INSERT INTO users (name, phone, email, login, password) '
            f'VALUES (?, ?, ?, ?, ?)',
            (form.name.data,
             form.phone.data,
             form.email.data,
             form.login.data,
             password))


def check_login(form):
    with sqlite3.connect('tic_tac.db', timeout=20) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        result = cursor.fetchall()

    for elem in result:
        if elem[-2] == form.login.data:
            return False
    return True


def check_login_and_password(form):
    with sqlite3.connect('tic_tac.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        result = cursor.fetchall()

    for elem in result:
        if elem[-2] == form.login.data and check_password_hash(elem[-1], form.password.data):
            return True
    return False


if __name__ == '__main__':
    pass
