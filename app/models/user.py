from database import db
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.VARCHAR(80))