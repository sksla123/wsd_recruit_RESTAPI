# routes/auth_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import auth_service

auth = Namespace('auth', description='Authentication related operations')

@auth.route('/register')
class UserRegister(Resource):
    """
    회원 가입 관련 API를 제공합니다.
    """
    def post(self):
        """
        회원 가입을 처리합니다.

        요청 본문에 회원 가입 데이터를 JSON 형식으로 포함해야 합니다.

        Returns:
            JsonResponse: 회원 가입 결과 데이터와 메시지
        """
        try:
            data, message = auth_service.register_user(request.json)
            return JsonResponse(data, message, HTTPStatus.CREATED).to_response()  # 201 Created
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@auth.route('/login')
class UserLogin(Resource):
    """
    로그인 관련 API를 제공합니다.
    """
    def post(self):
        """
        로그인을 처리합니다.

        요청 본문에 로그인 데이터를 JSON 형식으로 포함해야 합니다.

        Returns:
            JsonResponse: 로그인 결과 데이터와 메시지
        """
        try:
            data, message = auth_service.user_login(request.json)
            return JsonResponse(data, message).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@auth.route('/refresh')
class RefreshToken(Resource):
    """
    토큰 갱신 관련 API를 제공합니다.
    """
    def post(self):
        """
        토큰을 갱신합니다.

        요청 본문에 토큰 갱신 데이터를 JSON 형식으로 포함해야 합니다.

        Returns:
            JsonResponse: 토큰 갱신 결과 데이터와 메시지
        """
        try:
            data, message = auth_service.refresh_token(request.json)
            return JsonResponse(data, message).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)