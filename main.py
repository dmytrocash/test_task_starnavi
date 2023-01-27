import os
import datetime
from typing import Optional

from flask import Flask, abort, request, jsonify, make_response
from sqlalchemy.sql import text
from models import User, Post, Like

from db import db
from utils import validate_post_body, validate_signup_body, get_password_hash, \
    encode_user_data, decode_user_token


def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'developmentkey')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

    def user_authorization() -> Optional['User']:
        headers = request.headers
        if 'Authorization' not in headers:
            return
        authorization = headers['Authorization']
        token_type, token = authorization.split(' ')
        if token_type != 'Bearer':
            return
        user_decoded_data = decode_user_token(token, app.config["JWT_SECRET_KEY"])
        if 'id' not in user_decoded_data:
            return
        user = User.query.filter_by(id=user_decoded_data['id']).first()
        return user

    @app.route('/users', methods=['POST'])
    def user_signup():
        body, error = validate_signup_body(request.get_json())
        if error:
            abort(make_response({'message': error}, 401))
        if User.query.filter_by(email=body['email']).first() is not None:
            abort(make_response({
                'message': 'This email address already exists. Please choose'
                           ' a unique one.'}, 400))
        new_user = User(
            email=body['email'],
            password=get_password_hash(body['password'].strip())
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user)

    @app.route('/login', methods=['POST'])
    def user_login():    
        body, error = validate_signup_body(request.get_json())
        if error:
            abort(make_response({'message': error}, 400))

        password = body['password'].strip()
        email = body['email']
        user = User.query.filter_by(email=email, password=get_password_hash(password)).first()
        if user is None:
            abort(make_response({'message': 'Wrong email or password. Try again.'}, 401))

        user.last_login = datetime.datetime.now()
        db.session.commit()
        return encode_user_data(user.id, app.config["JWT_SECRET_KEY"])

    @app.route('/posts', methods=['POST'])
    def post_creation():
        user = user_authorization()
        if not user:
            abort(make_response({'message': 'You are not authorized.'}, 401))

        body, error = validate_post_body(request.get_json())
        if error:
            abort(make_response({'message': error}, 400))

        post = Post(
            text=body['text'],
            user_id=user.id
        )
        db.session.add(post)
        user.last_action = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return jsonify(post)

    @app.route('/posts/<int:post_id>/like', methods=['POST'])
    def post_like(post_id):
        user = user_authorization()
        if not user:
            abort(make_response({'message': 'You are not authorized.'}, 401))

        post = Post.query.filter_by(id=post_id).first()
        if post is None:
            abort(make_response({
                'message': 'Post with such id does not exist.'}, 400))

        like = Like.query.filter_by(user_id=user.id, post_id=post.id).first()
        if like is None:
            like = Like(
                user_id=user.id,
                post_id=post_id
            )
            db.session.add(like)
        
        user.last_action = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return jsonify(like)

    @app.route('/posts/<int:post_id>/unlike', methods=['POST'])
    def post_unlike(post_id):
        user = user_authorization()
        if not user:
            abort(make_response({'message': 'You are not authorized.'}, 401))

        post = Post.query.filter_by(id=post_id).first()
        if post is None:
            abort(make_response({
                'message': 'Post with such id does not exist.'}, 400))

        like = Like.query.filter_by(user_id=post.user_id, post_id=post.id).first()
        if like is not None:
            db.session.delete(like)
        
        user.last_action = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return {'message': 'You successfully unliked the post.'}, 200

    @app.route('/analytics', methods=['GET'])
    def analytics():
        user = user_authorization()
        if not user:
            abort(make_response({'message': 'Not Authorized'}, 401))

        args = request.args
        date_from = args.get('date_from', '2023-01-01')
        date_to = args.get('date_to', '2024-01-01')
        cmd = text(
            """
            SELECT COUNT(post_id) AS likes, strftime('%Y-%m-%d', created_at) AS date FROM "like" 
            WHERE created_at between :date_from and :date_to
            GROUP BY 2 
            """
        )
        cmd = cmd.bindparams(date_from=date_from, date_to=date_to)
        result = db.session.execute(cmd)
        return jsonify({'result': [dict(row) for row in result]})

    return app
