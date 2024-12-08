from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Login, LoginLog

db = SQLAlchemy()  # db 객체를 전역으로 선언하지 않음

def create_app():
    # Initialize Flask app and SQLAlchemy
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 연결 풀 옵션 추가
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 3600,  # 1시간마다 연결 재활용
        'pool_pre_ping': True,  # 연결 사용 전에 ping 테스트
    }

    db.init_app(app)  # db 객체 초기화

    # 앱 context 종료 시 연결 풀을 제거
    @app.teardown_appcontext
    def close_connection(exception):
        db.session.remove()
        db.engine.dispose()

    # Initialize API with Swagger documentation
    api = Api(app, version='1.0', title='Job Posting API',
              description='API for managing job postings',
              doc='/api-docs')

    # Import and register routes after initializing app and db
    from app.routes import auth
    api.add_namespace(auth.auth, path='/auth')

    # Initialize database tables (if needed)
    with app.app_context():
        db.create_all()

    return app