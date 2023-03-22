from database import db
from sqlalchemy.dialects.postgresql import UUID

AuthorsToBooks = db.Table(
    "authors_to_books",
    db.metadata,
    db.Column('book_id', UUID, db.ForeignKey("books.id")),
    db.Column('author_id', UUID, db.ForeignKey("authors.id"))
)
