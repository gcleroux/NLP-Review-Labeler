from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils.config import SQLiteConfig, INPUT_DIR, OUTPUT_DIR
from pathlib import Path

db = SQLAlchemy()


def create_app():
    # Init web server
    app = Flask(__name__)
    app.config.from_object(SQLiteConfig())
    db.init_app(app)

    # Create the in/out files
    Path(INPUT_DIR).mkdir(exist_ok=True)
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    from .labels import labels
    from .reviews import reviews
    from .uploads import uploads
    from .views import views

    # Routes for REST calls
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(uploads, url_prefix="/")
    app.register_blueprint(reviews, url_prefix="/")
    app.register_blueprint(labels, url_prefix="/")

    # Creating the db
    from . import models

    create_db(app)

    return app


def create_db(app):
    db.create_all(app=app)
