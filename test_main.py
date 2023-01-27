import pytest
from main import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_user_sign_up_success(client):
    response = client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    assert response.status_code == 200
    assert response.json["email"] == "example@example.com"


def test_user_sign_up_failed_user_exists(client):
    client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    response = client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    assert response.status_code == 400
    assert 'This email address already exists. Please choose ' \
           'a unique one.' in response.text


def test_sign_up_success(client):
    client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    response = client.post('/login', json={'email': 'example@example.com', 'password': '12345678'})
    assert response.status_code == 200
    assert response.json["token"] is not None


def test_sign_up_failed_short_password(client):
    response = client.post('/users', json={'email': 'example@example.com', 'password': '1234'})
    assert response.status_code == 400
    assert "Password should be more than 8 characters" in response.text


def test_email_doesnt_exist_login_failed(client):
    client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    response = client.post('/login', json={'email': 'example123@example.com', 'password': '12345678'})
    assert response.status_code == 401
    assert 'Wrong email. Try again.' in response.text


def test_post_create_success(client):
    client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    user_login = client.post('/login', json={'email': 'example@example.com', 'password': '12345678'})
    response = client.post('/posts', json={'text': 'text'}, headers={'Authorization': 'Bearer ' + user_login.json["token"]})
    assert response.status_code == 200
    assert response.json["text"] is not None


def test_like_post_success(client):
    client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    user_login = client.post('/login', json={'email': 'example@example.com', 'password': '12345678'})
    client.post('/posts', json={'text': 'text'}, headers={'Authorization': 'Bearer ' + user_login.json["token"]})
    response = client.post('/posts/1/like', headers={'Authorization': 'Bearer ' + user_login.json["token"]})
    assert response.status_code == 200
    assert response.json["id"] is not None


def test_unlike_post_success(client):
    client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    user_login = client.post('/login', json={'email': 'example@example.com', 'password': '12345678'})
    client.post('/posts', json={'text': 'text'}, headers={'Authorization': 'Bearer ' + user_login.json["token"]})
    client.post('/posts/1/like', headers={'Authorization': 'Bearer ' + user_login.json["token"]})
    response = client.post('/posts/1/unlike', headers={'Authorization': 'Bearer ' + user_login.json["token"]})
    assert response.status_code == 200
    assert 'You successfully unliked the post.' in response.text


def test_like_non_existing_post_failed(client):
    client.post('/users', json={'email': 'example@example.com', 'password': '12345678'})
    user_login = client.post('/login', json={'email': 'example@example.com', 'password': '12345678'})
    response = client.post('/posts/1/like', headers={'Authorization': 'Bearer ' + user_login.json["token"]})
    assert response.status_code == 400
    assert 'Post with such id does not exist.' in response.text
