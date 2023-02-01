from dataclasses import dataclass
from sqlalchemy.sql import func
from db import db


@dataclass
class User(db.Model):
    id: int
    email: str
    created_at: str
    last_login: str
    last_action: str

    id = db.Column(db.Integer, primary_key=True)
    # TODO: make index
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)
    last_action = db.Column(db.DateTime(timezone=True), nullable=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)


@dataclass
class Post(db.Model):
    id: int
    text: str
    user_id: int
    created_at: str

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), nullable=False)
    likes = db.relationship('Like', backref='post', lazy=True)


@dataclass
class Like(db.Model):
    id: int
    user_id: int
    post_id: int
    created_at: str

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), nullable=False)
