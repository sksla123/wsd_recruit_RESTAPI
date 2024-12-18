from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import auth_service
from ..views.response import *
from ..utils.util import calculate_remaining_time
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

auth = Namespace('auth', description='Authentication related operations')

# Request models
register_model = auth.model('RegisterModel', {
    'user_id': fields.String(required=True, example='example_user'),
    'user_email': fields.String(required=True, example='example_user@example.com'),
    'user_password': fields.String(required=True, example='examplePassword123'),
    'user_level': fields.Integer(required=True, example=10)
})

login_model = auth.model('LoginModel', {
    'user_id': fields.String(required=True, example='example_user'),
    'user_password': fields.String(required=True, example='examplePassword123')
})

logout_model = auth.model('LogoutModel', {
    'refresh_token': fields.String(required=True, example='abcdefghijkmnlopqrstuvwxyz')
})

refresh_model = auth.model('RefreshModel', {
    'user_id': fields.String(required=True, example='example_user'),
    'refresh_token': fields.String(required=True, example='abcdefghijkmnlopqrstuvwxyz')
})

profile_update_model = auth.model('ProfileUpdateModel', {
    'user_id': fields.String(required=True, example='example_user'),
    'action': fields.String(required=True, example='password'),
    'new_value': fields.String(required=True, example='newSecurePassword123')
})

@auth.route('/register')
class UserRegister(Resource):
    @auth.expect(register_model)
    def post(self):
        """회원 가입을 처리합니다."""
        try:
            # print(request.json)
            success, data, message, status = auth_service.register_user(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))

@auth.route('/login')
class UserLogin(Resource):
    @jwt_required(optional=True)
    def post(self):
        """로그인을 처리합니다."""
        try:
            current_user = get_jwt_identity()
            if current_user:
                token_dict = get_jwt()
                remaining_time = calculate_remaining_time(token_dict)
                message = f"이미 로그인 되어있습니다. 토큰 만료까지 남은 시간: {remaining_time:.2f}초"
                return fail(message, 400)
            success, data, message, status = auth_service.user_login(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))

@auth.route('/logout')
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        """로그아웃을 처리합니다."""
        try:
            current_user = get_jwt_identity()
            print(current_user)
            if not current_user:
                message = "로그인 먼저 해주세요."
                return fail(message, 400)
            success, data, message, status = auth_service.user_logout(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))

@auth.route('/refresh')
class RefreshToken(Resource):
    def post(self):
        """토큰을 갱신합니다."""
        try:
            success, data, message, status = auth_service.refresh_token(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))

@auth.route('/profile')
class UserProfile(Resource):
    def put(self):
        """회원정보를 수정합니다."""
        try:
            success, data, message, status = auth_service.update_user_profile(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))
