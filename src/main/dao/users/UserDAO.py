from src.main.model.model_utils.ModelUtils import db
from src.main.model.User import User


# ====== DAO class, responsible for querying the DB in the user namespace


class UserDAO():
    def get_all_users():
        return User.query.all()

    def create_user(user):
        db.session.add(user)
        db.session.commit()

    def get_user_by_username(name):
        user_with_username = User.query.filter_by(username=name).first()
        return user_with_username

    def user_exists_by_username(name):
        return UserDAO.get_user_by_username(name) is not None
