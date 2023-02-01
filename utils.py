import jwt
import bcrypt
import re


# TODO: env var
SALT = b'$2b$12$LxwRsweKXFfzmu/vk4S8AO'


def get_password_hash(password):
    return bcrypt.hashpw(password.encode(), SALT).decode('utf-8')


def encode_user_data(user_id, secret_key):
    encoded_jwt = jwt.encode({"id": user_id}, secret_key, algorithm="HS256")
    return {'token': encoded_jwt}


def decode_user_token(token, secret_key):
    data = jwt.decode(token, secret_key, algorithms="HS256")
    return data


def validate_signup_body(body):
    if 'email' not in body or 'password' not in body:
        return None, 'Email or Password fields are missing'
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", body['email']):
        return None, 'Invalid email'
    if len(body['password']) < 8:
        return None, 'Password should be more than 8 characters'
    return body, None


def validate_post_body(body):
    if 'text' not in body:
        return None, 'Text field is missing'
    return body, None
