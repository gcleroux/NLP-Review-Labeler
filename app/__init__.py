from genericpath import exists
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils.config import DockerConfig, LocalConfig, UPLOAD_DIR
from pathlib import Path

db = SQLAlchemy()

def create_app():
    # Init du serveur web
    app = Flask(__name__)
    app.config.from_object(LocalConfig())
    db.init_app(app)
    
    # Create the input_files dir
    Path(UPLOAD_DIR).mkdir(exist_ok=True)
    
    from .views import views
    
    # Enregistrements des routes pour les appels REST
    app.register_blueprint(views, url_prefix='/')
    
    # Creation de la database
    from . import models
    create_db(app)   
    
    return app

def create_db(app):
    db.create_all(app=app)
