import pytest
from src.config import TestingConfig
from src.CreateApp import create_application
from src.tests.samples import s_user_1, s_user_2, s_post_1, s_post_2, s_comment_1, s_comment_2
from flask_jwt_extended import create_access_token

# ====== Fixtures to happen before and after IT tests


@pytest.fixture(scope='session')
def app_db():
    # === Creating the application and db
    appdb = create_application(TestingConfig)
    return appdb


@pytest.fixture(scope='session')
def app(app_db):
    # === Getting the application
    return app_db[0]


@pytest.fixture(scope='session')
def db(app, app_db):
    # === Filling the db with sample data & getting it
    db = app_db[1]
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(s_user_1)
        db.session.add(s_user_2)
        db.session.add(s_post_1)
        db.session.add(s_post_2)
        db.session.add(s_comment_1)
        db.session.add(s_comment_2)
        db.session.commit()
    yield db
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    # === Getting the test client
    return app.test_client()


@pytest.fixture(scope='session')
def token_1(app, db):
    # === Getting the token that identifies user 1
    with app.app_context():
        tok = create_access_token(identity=1)
    return tok


@pytest.fixture(scope='session')
def token_2(app, db):
    # === Getting the token that identifies user 2
    with app.app_context():
        tok = create_access_token(identity=2)
    return tok
