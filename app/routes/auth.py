from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import auth_service
from app.utils import responses
from app.middlewares import auth_middleware

auth = Namespace('auth', description='Authentication related operations')

# Request and Response Models for Swagger documentation
user_register_model = auth.model('UserRegister', {
    'user_email': fields.String(required=True, description='User email'),
    'user_password': fields.String(required=True, description='User password'),
})

user_login_model = auth.model('UserLogin', {
    'user_email': fields.String(required=True, description='User email'),
    'user_password': fields.String(required=True, description='User password'),
})

user_profile_update_model = auth.model('UserProfileUpdate', {
    'user_password': fields.String(description='New user password'),
    # Add other profile fields here if needed
})

token_refresh_model = auth.model('TokenRefresh', {
    'refresh_token': fields.String(required=True, description='Refresh token')
})

@auth.route('/register')
class UserRegister(Resource):
    @auth.expect(user_register_model)
    @auth.response(201, 'User registered successfully', responses.response_model)
    @auth.response(400, 'Bad request', responses.error_model)
    def post(self):
        """Register a new user"""
        return auth_service.register_user(request.json)

@auth.route('/login')
class UserLogin(Resource):
    @auth.expect(user_login_model)
    @auth.response(200, 'Login successful', responses.token_model)
    @auth.response(401, 'Unauthorized', responses.error_model)
    def post(self):
        """Login a user"""
        return auth_service.login_user(request.json)

@auth.route('/refresh')
class TokenRefresh(Resource):
    @auth.expect(token_refresh_model)
    @auth.response(200, 'Token refreshed successfully', responses.token_model)
    @auth.response(401, 'Unauthorized', responses.error_model)
    def post(self):
        """Refresh access token"""
        return auth_service.refresh_token(request.json)

@auth.route('/profile')
class UserProfile(Resource):
    @auth_middleware.auth_required
    @auth.expect(user_profile_update_model)
    @auth.response(200, 'Profile updated successfully', responses.response_model)
    @auth.response(400, 'Bad request', responses.error_model)
    @auth.response(401, 'Unauthorized', responses.error_model)
    def put(self):
        """Update user profile"""
        return auth_service.update_user_profile(request.json)