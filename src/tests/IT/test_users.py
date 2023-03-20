from src.tests.conftests import app_db, app, db, client, token_1, token_2
from src.main.model.User import User
import copy

new_user = {'username': 'new-user', 'password': 'new-password'}

# =============== IT tests in the user namespace


def test_no_auth_should_fail(client):
    response = client.get('/user/')
    assert response.status_code == 401


def test_bad_auth_should_fail(client, token_1):
    response = client.get('/user/',
                          headers={'Authorization': f'Bearer {token_1[:-1]}'})
    assert response.status_code == 422


def test_create_new_user_should_succeed(client, app):
    response = client.post('/user/',
                           json=new_user)
    assert response.status_code == 201
    with app.app_context():
        assert User.query.first().username == new_user['username']


def test_create_new_user_with_duplicate_username_should_fail(client, app):
    response = client.post('/user/',
                           json=new_user)
    assert response.status_code == 400


def test_create_new_user_with_missing_field_should_fail(client, app):
    temp_creds = copy.deepcopy(new_user)
    del temp_creds['username']
    response = client.post('/user/',
                           json=temp_creds)
    assert response.status_code == 400
    assert 'required' in response.json['errors']['username']


def test_create_new_user_with_empty_field_should_fail(client, app):
    temp_creds = copy.deepcopy(new_user)
    temp_creds['password'] = ''
    response = client.post('/user/',
                           json=temp_creds)
    assert response.status_code == 400
    assert 'empty' in response.json['errors']['password']


def test_login_should_succeed(client, app):
    response = client.post('/user/login',
                           json=new_user)
    assert response.status_code == 200
    assert 'token' in response.json


def test_login_bad_username_should_fail(client, app):
    bad_user = {'username': 'not-exist', 'password': 'new-password'}
    response = client.post('/user/login',
                           json=bad_user)
    assert response.status_code == 400


def test_login_bad_password_should_fail(client, app):
    bad_user = {'username': 'new-user', 'password': 'bad-password'}
    response = client.post('/user/login',
                           json=bad_user)
    assert response.status_code == 400
