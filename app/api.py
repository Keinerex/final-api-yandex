from uuid import UUID

from flask import Blueprint

from models import Category, Book, Genre, Author, Review, User
from database import db
from flask import jsonify, request

bp = Blueprint('api', __name__)


@bp.route("/categories", methods=["GET"])
def categories():
    return jsonify([
        {
            "id": str(category.id),
            "title": str(category.title),
            "books": [
                str(book.id) for book in db.session.query(Book).filter(Book.category_id == category.id)
            ]
        } for category in db.session.query(Category).all()])


@bp.route("/books/", methods=["GET"])
def books():
    args = request.args
    category_id = UUID(args.get("category_id"))
    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "price": book.price,
            "annotation": book.annotation,
            "genre": db.session.query(Genre).filter(Genre.id == book.genre_id).first().title,
            "authors": [str(author.name) for author in
                        db.session.query(Author).filter(Author.books.any(id=book.id)).all()],
            "reviews": [str(review.id) for review in db.session.query(Review).filter(Review.book_id == book.id).all()]
        } for book in db.session.query(Book).all() if book.category_id == category_id])


@bp.route("/reviews/", methods=["GET"])
def reviews():
    args = request.args
    book_id = UUID(args.get("book_id"))
    return jsonify([
        {
            "id": review.id,
            "rate": review.rate,
            "text": review.text,
            "user": db.session.query(User).filter(User.id == review.user_id).first().name
        } for review in db.session.query(Review).all() if review.book_id == book_id])


@bp.route("/book/", methods=["GET"])
def book():
    args = request.args
    book_id = UUID(args.get("book_id"))
    book = db.session.query(Book).filter(Book.id == book_id).first()
    return jsonify(
        {
            "id": book.id,
            "title": book.title,
            "price": book.price,
            "annotation": book.annotation,
            "genre": db.session.query(Genre).filter(Genre.id == book.genre_id).first().title,
            "authors": [str(author.name) for author in
                        db.session.query(Author).filter(Author.books.any(id=book.id)).all()],
            "reviews": [str(review.id) for review in db.session.query(Review).filter(Review.book_id == book.id).all()]
        })
