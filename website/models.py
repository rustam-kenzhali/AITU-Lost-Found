from . import db   # import from website folder
from flask_login import UserMixin
from sqlalchemy.sql import func

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    content = db.Column(db.String(10000))
    lostfound = db.Column(db.String(50))
    category = db.Column(db.String(100))
    image = db.Column(db.String(1000))
    author = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    group = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))

    posts = db.relationship('Post')


