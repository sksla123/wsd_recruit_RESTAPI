from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # 설정 로드
    db_config = Config.get_db_config()
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_config['MySQL']['user']}:{db_config['MySQL']['password']}@{db_config['MySQL']['url']}:{db_config['MySQL']['port']}/dbname"
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    
    # 확장 초기화
    db.init_app(app)
    jwt.init_app(app)
    Swagger(app)
    
    # 블루프린트 등록
    from .routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app