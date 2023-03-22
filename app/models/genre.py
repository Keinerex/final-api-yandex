from database import db
from .base import BaseModel


class Genre(BaseModel):
    __tablename__ = "genres"

    title = db.Column(db.String(80))
