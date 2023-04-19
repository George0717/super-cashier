from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from ..database.base import Base

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(25), nullable=False)

    def __init__(self, email="", name="", password=""):
        self.email = email
        self.name = name
        self.password = password

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

    def welcome_user(self):
        return f'--- Selamat datang, {self.name}! ---'
    