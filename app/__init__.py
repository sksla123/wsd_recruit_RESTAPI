from flask import Flask
from flask_injector import FlaskInjector
from injector import singleton

from .config import Config
from .main import main as main_blueprint
from .auth import auth as auth_blueprint

# blueprint 등록
def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(test_blueprint)
    app.register_blueprint(auth_blueprint)

    def configure(binder):
        binder.bind(DataService, to=DataService, scope=singleton)
    
    FlaskInjector(app=app, modules=[configure])

    return app
