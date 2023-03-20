from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_jwt_extended import JWTManager

import os
from src.main.controller.users.UserController import user_ns
from src.main.controller.posts.PostController import blogpost_ns
from src.config import DevelopmentConfig
from flask_migrate import Migrate
from src.main.model.model_utils.ModelUtils import db, cache
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


# Application factory - creating, configuring and returning an application based on a configuration
def create_application(config):
    app = Flask(__name__)

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)

    app.config.from_object(config)
    jwt = JWTManager(app)
    api = Api(app)

    db.init_app(app)
    cache.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    api.add_namespace(blogpost_ns, path='/blogpost')
    api.add_namespace(user_ns, path='/user')

    # === cheat? just kidding ;) dont need it
    # @api.errorhandler(Exception)
    # def handle_server_exception(error):
    #    return {'message': 'Something went wrong...'}, 400

    return app, db
