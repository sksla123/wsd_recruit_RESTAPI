from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from Config class
    from config import Config
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_db_uri()
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints (routes)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app