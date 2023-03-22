from sqlalchemy.dialects.postgresql import BIGINT
from database import db
from .base import BaseModel


class Book(BaseModel):
    __tablename__ = "books"

    category_id = db.Column(db.ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    genre_id = db.Column(db.ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.VARCHAR(80), nullable=False)
    price = db.Column(BIGINT, nullable=False)
    annotation = db.Column(db.TEXT, nullable=False, default="Для данного товара нет описания")

    authors = db.relationship("Author", secondary="authors_to_books", backref="books")