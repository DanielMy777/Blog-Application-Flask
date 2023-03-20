import pytest
from pytest_mock import mocker
from src.tests.conftests import app_db, app
from src.main.service.users.UserService import UserService
from src.main.dao.users.UserDAO import UserDAO
from src.main.model.User import User
from werkzeug.security import generate_password_hash

sample_users = [{'username': 'user1', 'password': 'pass1'},
                {'username': 'user2', 'password': 'pass2'}]

# ====== Unit tests in the user namespace


def test_get_all_users_should_return(mocker):
    # arrange
    users = sample_users
    mocker.patch.object(UserDAO, 'get_all_users', return_value=users)
    # act
    result = UserService.get_all_users()
    # assert
    assert len(result) == 2
    assert result[0]['username'] == 'user1'
    assert result[1]['username'] == 'user2'


def test_create_user_should_pass(mocker):
    # arrange
    s_user = sample_users[0]
    mocker.patch.object(UserDAO, 'user_exists_by_username', return_value=False)
    mocker.patch.object(UserDAO, 'create_user', return_value=None)
    # act
    result = UserService.create_user(s_user['username'], s_user['password'])
    # assert
    assert result is None


def test_create_user_with_duplicate_username_should_throw(mocker):
    # arrange
    s_user = sample_users[0]
    mocker.patch.object(UserDAO, 'user_exists_by_username', return_value=True)
    mocker.patch.object(UserDAO, 'create_user', return_value=None)
    # act
    with pytest.raises(Exception) as e:
        UserService.create_user(s_user['username'], s_user['password'])
    # assert
    assert e._excinfo[0].code == 400


def test_login_should_pass(app, mocker):
    # arrange
    s_user = sample_users[0]
    with app.app_context():
        user = User(s_user['username'],
                    generate_password_hash(s_user['password']))
        mocker.patch.object(UserDAO, 'get_user_by_username', return_value=user)
    # act
        result = UserService.auth_user(s_user['username'], s_user['password'])
    # assert
    assert result is not None


def test_login_bad_username_should_throw(app, mocker):
    # arrange
    s_user = sample_users[0]
    with app.app_context():
        mocker.patch.object(UserDAO, 'get_user_by_username', return_value=None)
    # act
        with pytest.raises(Exception) as e:
            UserService.auth_user(
                s_user['username'], s_user['password'])
    # assert
    assert e._excinfo[0].code == 400


def test_login_bad_password_should_throw(app, mocker):
    # arrange
    s_user = sample_users[0]
    with app.app_context():
        user = User(s_user['username'],
                    'bad-pass')
        mocker.patch.object(UserDAO, 'get_user_by_username', return_value=user)
    # act
        with pytest.raises(Exception) as e:
            UserService.auth_user(
                s_user['username'], s_user['password'])
    # assert
    assert e._excinfo[0].code == 400
