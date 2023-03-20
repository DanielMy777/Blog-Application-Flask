from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from src.main.dao.users.UserDAO import UserDAO
from src.main.model.User import User

# === Service class, responsible of handling the business login in the user namespace


class UserService():
    def get_all_users():
        return UserDAO.get_all_users()

    def create_user(username, password):
        if not UserDAO.user_exists_by_username(username):
            pw_hash = generate_password_hash(password)
            user = User(username, pw_hash)
            UserDAO.create_user(user)
        else:
            abort(400, f"User with username '{username}' already exists.")

    def auth_user(username, password):
        user = UserDAO.get_user_by_username(username)
        if user is not None:
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                return access_token
        abort(400, f"Username or password incorrect!")
