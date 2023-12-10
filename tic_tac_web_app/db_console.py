from sqlalchemy import  create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


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
