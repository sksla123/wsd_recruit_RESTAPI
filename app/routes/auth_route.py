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
    'user_id': fields.String(required=True, description='사용자 아이디. 영문, 숫자 조합으로 4-20자', example='example_user'),
    'user_email': fields.String(required=True, description='사용자 이메일 주소', example='example_user@example.com'),
    'user_password': fields.String(required=True, description='사용자 비밀번호. 영문, 숫자, 특수문자 조합으로 8-20자', example='examplePassword123'),
    'user_level': fields.Integer(required=True, description='사용자 레벨. 5,10 둘 중 하나\n10: 일반 사용자, 5: 회사측 사용자', example=10)
})

login_model = auth.model('LoginModel', {
    'user_id': fields.String(required=True, description='사용자 아이디', example='example_user'),
    'user_password': fields.String(required=True, description='사용자 비밀번호', example='examplePassword123')
})

logout_model = auth.model('LogoutModel', {
    'refresh_token': fields.String(required=True, description='로그아웃할 리프레시 토큰', example='abcdefghijkmnlopqrstuvwxyz')
})

refresh_model = auth.model('RefreshModel', {
    'user_id': fields.String(required=True, description='사용자 아이디', example='example_user'),
    'refresh_token': fields.String(required=True, description='갱신할 리프레시 토큰', example='abcdefghijkmnlopqrstuvwxyz')
})

profile_update_model = auth.model('ProfileUpdateModel', {
    'user_id': fields.String(required=True, description='수정할 사용자 아이디', example='example_user'),
    'action': fields.String(required=True, description='수정 작업 유형 (예: password, email)', example='password'),
    'new_value': fields.String(required=True, description='새로운 값(변경할 패스워드, 이메일)', example='newSecurePassword123')
})

@auth.route('/register')
class UserRegister(Resource):
    @auth.doc(
        security=None,
        responses={
            HTTPStatus.OK.value: '''
{
  "status": "success",
  "message": "회원 가입에 성공하셨습니다.",
  "data": {
    "user_id": "example_user",
    "user_email": "example_user@example.com",
    "user_level": 10,
    "created_date": "2024-12-18T21:56:07"
  }
}
''',
            400: '''
{
  "status": "failed",
  "message": "잘못된 user_level입니다. 5(company user) 또는 10(normal user)만 가능합니다."
}
''',
        }
    ) 
    @auth.expect(register_model)
    def post(self):
        """회원 가입을 처리합니다."""
        try:
            success, data, message, status = auth_service.register_user(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))

@auth.route('/login')
class UserLogin(Resource):
    @auth.doc(
        security=None,
        responses={
            HTTPStatus.OK.value: '''
{
  "status": "success",
  "message": "회원 가입에 성공하셨습니다.",
  "data": {
    "user_id": "example_user",
    "user_email": "example_user@example.com",
    "user_level": 10,
    "created_date": "2024-12-18T21:56:07"
  }
}
''',
            400: '''
{
  "status": "failed",
  "message": "사용자를 찾을 수 없습니다.",
  "data": {}
}
''',
        }
    ) 
    @auth.expect(login_model)
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
    @auth.doc(
        responses={
            HTTPStatus.OK.value: '''
{
  "status": "success",
  "message": "Successfully logout",
  "data": {}
}
''',
            400: '''
{
  "status": "failed",
  "message": "로그인된 token이 없습니다.",
  "data": {}
}
''',
        }
    ) 
    @jwt_required()
    @auth.expect(logout_model)
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
    @auth.doc(
        security=None,
        responses={
            HTTPStatus.OK.value: '''
{
  "status": "success",
  "message": {
    "user_id": "example_user",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNDUyNjk1NCwianRpIjoiYjg5M2RjYWQtZDllMC00NWY0LWE4ZjMtNWUzNmQ3ODQ1NzFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImV4YW1wbGVfdXNlciIsIm5iZiI6MTczNDUyNjk1NCwiY3NyZiI6IjliNzlkNDM0LTQzYjUtNDgxOS1iYTFkLTJkYWJlMzI5MTYyNiIsImV4cCI6MTczNDUyNzg1NH0.kq_eyz1wNPL3q3eO6Z8m6_CmI1FNFINMuqcSsLqbQvA"
  },
  "data": "토큰 갱신 성공"
}
''',
            401: '''
{
  "status": "failed",
  "message": {},
  "data": "로그인된 사용자를 찾을 수 없습니다."
}
''',
        }
    ) 
    @auth.expect(refresh_model)
    def post(self):
        """토큰을 갱신합니다."""
        try:
            success, data, message, status = auth_service.refresh_token(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))

@auth.route('/profile')
class UserProfile(Resource):
    @auth.doc(
        responses={
            HTTPStatus.OK.value: '''
{
  "status": "success",
  "message": "password 업데이트에 성공했습니다.",
  "data": {
    "user_id": "example_user",
    "updated_field": "password",
    "new_value": "******"
  }
}
''',
            404: '''
{
  "status": "failed",
  "message": "사용자를 찾을 수 없습니다."
}
''',
        }
    )
    @auth.expect(profile_update_model)
    def put(self):
        """회원정보를 수정합니다."""
        try:
            success, data, message, status = auth_service.update_user_profile(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))
