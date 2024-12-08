from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flasgger import Swagger

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    Swagger(app)

    # Register blueprints
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app