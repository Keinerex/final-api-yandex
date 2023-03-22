from database import db
from .base import BaseModel

from sqlalchemy.dialects.postgresql import SMALLINT


class Review(BaseModel):
    __tablename__ = "reviews"

    book_id = db.Column(db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    rate = db.Column(SMALLINT, nullable=False)
    text = db.Column(db.TEXT, nullable=False)

