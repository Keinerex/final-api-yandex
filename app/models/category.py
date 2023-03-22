from database import db
from .base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    title = db.Column(db.VARCHAR(80))
