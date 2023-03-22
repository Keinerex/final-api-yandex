from database import db
from .base import BaseModel


class Author(BaseModel):
    __tablename__ = "authors"

    name = db.Column(db.VARCHAR(80), nullable=False)
