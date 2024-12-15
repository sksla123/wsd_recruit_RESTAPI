from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    print(app.config['JWT_ACCESS_TOKEN_EXPIRES'])

    api = Api(app,
              version='1.0',
              title='Recruilting Backend REST API',
              description='API for Recreuilting Backend',
              doc='/api-docs',
              add_specs=False,
              )

    # 인증 미드웨어 추가    
    from app.middlewares.auth_guard import AuthGuard
    AuthGuard.init_app(app)
        
    # 라우트 추가
    from app.routes import auth_route, application_route, job_route, bookmark_route
    api.add_namespace(auth_route.auth, path='/auth')
    api.add_namespace(application_route.application, path='/applications')
    api.add_namespace(job_route.job, path='/jobs')
    api.add_namespace(bookmark_route.bookmark, path='/bookmarks')

    print(app.url_map)
    return app
