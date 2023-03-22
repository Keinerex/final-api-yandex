import os

from flask import Flask
import models
from database import db
from api import bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  r"postgresql://postgres:Pa$$word@localhost:5432/base")
app.config["JSON_AS_ASCII"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(bp, url_prefix="/api")

if __name__ == "__main__":
    app.run()
