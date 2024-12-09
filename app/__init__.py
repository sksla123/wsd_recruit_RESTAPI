from flask import Flask
from flask_restx import Api, Resource

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 3600,  # 1시간마다 연결 재활용
        'pool_pre_ping': True,  # 연결 사용 전에 ping 테스트
    }

    # Initialize API with Swagger documentation
    api = Api(app, version='1.0', title='Recruilting Backend REST API',
              description='API for Recreuilting Backend',
              doc='/api-docs',
              add_specs=False
              )
    
    # # 루트 경로에 대한 GET 요청 처리
    # class Root(Resource): 
    #     def get(self):
    #         return {"message": "Hello!"}
        
    # # 루트 경로에 Resource 등록 (엔드포인트 명시)
    # api.add_resource(Root, '/', endpoint='root_endpoint')
    print(app.url_map)
    print(api.endpoints)

    # Import and register routes after initializing app and db
    from app.routes import auth
    api.add_namespace(auth.auth, path='/auth')

    return app
