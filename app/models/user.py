import json

from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.VARCHAR(80))
    name = db.Column(db.VARCHAR(80))
    surname = db.Column(db.VARCHAR(80))
    patronymic = db.Column(db.VARCHAR(80))
    email = db.Column(db.String(120), unique=True)
    tel = db.Column(db.String(18), unique=True)
    password_hash = db.Column(db.String(128))
    cart = db.Column(db.Text())
    date = db.Column(db.VARCHAR(10))

    @property
    def data(self):
        return {
            "username": self.username,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
            "email": self.email,
            "tel": self.tel,
            "date": self.date,
            "cart": json.loads(self.cart)
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
