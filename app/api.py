import datetime
import json
from uuid import UUID

from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, \
    current_user, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash

from database import db
from models import Category, Book, Genre, Author, Review, User

bp = Blueprint('api', __name__)

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.datetime.now(datetime.timezone.utc)
        target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            print("new token")
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    try:
        user = User.query.filter_by(username=username).one_or_none()
    except Exception as e:
        return jsonify({"msg": "error"})

    if not user or not user.check_password(password):
        return jsonify({"status": False}), 401

    response = jsonify({"status": True})
    access_token = create_access_token(identity=user.id)
    set_access_cookies(response, access_token)
    return response


@bp.route("/user_existed", methods=["GET"])
def user_existed():
    username = request.json.get("username", None)
    user = User.query.filter_by(username=username).one_or_none()
    if not user:
        return jsonify({"status": False})

    return jsonify({"status": True})


@bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()

    if not user and username and password:
        db.session.add(User(username=username, password_hash=generate_password_hash(password),
                            cart=json.dumps({"books": {}, "price": 0})))
        db.session.commit()
        return jsonify({"status": True})

    return jsonify({"status": False})


@bp.route("/logout", methods=["POST"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@bp.route("/get_user_data", methods=["GET"])
@jwt_required()
def get_user_data():
    return jsonify(current_user.data)


@bp.route("/is_authorized", methods=["GET"])
@jwt_required()
def is_authorized():
    return jsonify({"status": True})


@bp.route("/update_cart", methods=["PUT"])
@jwt_required()
def update_cart():
    cart = request.json.get("cart", None)
    if cart:
        current_user.cart = json.dumps(cart)
        db.session.commit()
        return jsonify({"msg": "cart was updated"})
    return jsonify({"msg": "error"})


@bp.route("/update_userdata", methods=["PUT"])
@jwt_required()
def update_userdata():
    name = request.json.get("name", None)
    surname = request.json.get("surname", None)
    patronymic = request.json.get("patronymic", None)
    email = request.json.get("email", None)
    tel = request.json.get("tel", None)
    date = request.json.get("date", None)
    if name and surname and email and tel and date:
        current_user.patronymic = patronymic
        current_user.surname = surname
        current_user.name = name
        current_user.email = email
        current_user.tel = tel
        current_user.date = date
        db.session.commit()
        return jsonify({"status": True})
    return jsonify({"status": False})


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
