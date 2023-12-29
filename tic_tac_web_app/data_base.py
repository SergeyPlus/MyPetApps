import sqlite3
from typing import List, Tuple

from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash
import logging


db_logger = logging.getLogger('db_logger')
db_logger.propagate = False

engine = create_engine("sqlite:///tic_tac.db", connect_args={"timeout": 30})
Session = sessionmaker(bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str]
    login: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.phone}, {self.email}, {self.login}, {self.password}'


Base.metadata.create_all(engine)


class UserDb:
    def __init__(self, response: Tuple):
        self.id = response[0]
        self.name = response[1]
        self.phone = response[2]
        self.email = response[3]
        self.login = response[4]
        self.password = response[5]

    def __getitem__(self, item):
        """
        It allows to take items from UserDb instanca in acoordance with Dict approach
        """
        return getattr(self, item)


class UserDbInterface:

    @classmethod
    def _get_cursor(cls):
        """
        Just set connection with DB
        """
        with sqlite3.Connection('tic_tac.db') as conn:
            cursor: sqlite3.Cursor = conn.cursor()
        return cursor

    @classmethod
    def get_user_data(cls, login) -> UserDb:
        """
        Get from tic_tac.db information about User based on received login
        """
        cursor = cls._get_cursor()
        select_req: str = f'SELECT * FROM users WHERE login = ?'
        cursor.execute(select_req, (login, ))
        result = cursor.fetchall()
        db_logger.info(f'Result from DB tic_tac.db {result}')
        if result:
            db_instance: UserDb = UserDb(result[0])
            return db_instance

    @classmethod
    def update_password(cls, login, password) -> None:
        """
        Updates password of User based on login
        """
        cursor = cls._get_cursor()
        update_req: str = f'UPDATE users SET password = ? WHERE login = ?'
        cursor.execute(update_req, (password, login))

    @classmethod
    def add_data_to_database(cls, form):
        """
        Add data about User based on validated form
        """
        password = generate_password_hash(form.password.data)
        cursor = cls._get_cursor()
        cursor.execute(
            f'INSERT INTO users (name, phone, email, login, password) '
            f'VALUES (?, ?, ?, ?, ?)',
            (form.name.data,
             form.phone.data,
             form.email.data,
             form.login.data,
             password))


if __name__ == '__main__':
    ...
