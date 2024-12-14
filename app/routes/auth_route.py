# routes/auth_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import auth_service

auth = Namespace('auth', description='Authentication related operations')

@auth.route('/register')
class UserRegister(Resource):
    def post(self):

        return auth_service.register_user(request.json)
    
@auth.route('/login')
class UserLogin(Resource):
    def post(self):

        return auth_service.user_login(request.json)
    
@auth.route('/refresh')
class RefreshToken(Resource):
    def post(self):
    
        return auth_service.refresh_token(request.json)

@auth.route('/profile')
class Profile(Resource):
    def put(self):

        return auth_service.update_user_profile(request.json)