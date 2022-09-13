import os
from pathlib import Path

APP_DIR = Path(os.path.abspath(os.path.dirname(__file__))).parent.absolute()
UPLOAD_DIR = os.path.join(APP_DIR, "input_files")

class DockerConfig(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@postgres_db_container:5432/ift585'


class LocalConfig(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
