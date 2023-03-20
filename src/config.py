import os
from datetime import timedelta
from dotenv import load_dotenv

# ====== Creating configuration classes for each purpose of the app.

# === Loading env variable defaults
load_dotenv()
# === Getting base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# NEEDED ENV VARS =================
# os.environ["POSTGRES_SERVICE"] = 'localhost:5431'
# os.environ["POSTGRES_USER"] = 'postgres'
# os.environ["POSTGRES_PASSWORD"] = 'postgres'
# os.environ["CACHE_REDIS_PORT"] = "6379"
# os.environ["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
# ==============================


# === Creating postgres connection string
POSTGRES_SERVICE = os.environ['POSTGRES_SERVICE']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_CONN_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVICE}"


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True
    JWT_SECRET_KEY = 'u7lJobSQUYkf64LWpA9osdd8bRXHdfUOc+RTN8Pg3FE='
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    CACHE_REDIS_DB = "0"
    CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = "500"
    RESTX_MASK_SWAGGER = False


# === Configuration for production (Not used in this app)
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = POSTGRES_CONN_URI + '/BlogAppProd'


# === Configuration for development
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = POSTGRES_CONN_URI + '/BlogAppDev'


# === Configuration for testing
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = POSTGRES_CONN_URI + '/BlogAppTest'
