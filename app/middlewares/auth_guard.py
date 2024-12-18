# app/middlewares/auth_guard.py
from flask import request, jsonify, current_app, g
from flask_jwt_extended import JWTManager, verify_jwt_in_request, jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from datetime import timedelta
from ..views.response import JsonResponse, fail
from ..models.database import get_db
from ..models.login import Login, get_login_by_user_id, create_login, delete_login
from ..utils.util import now_korea
from functools import wraps

jwt = JWTManager()

class AuthGuard:
    """인증 및 권한 부여를 관리하는 클래스"""

    EXCLUDED_ENDPOINTS = {
        'root': ['OPTIONS', 'HEAD', 'GET'],
        'specs': ['OPTIONS', 'HEAD', 'GET'],
        'restx_doc.static': ['OPTIONS', 'HEAD', 'GET'],
        'doc': ['OPTIONS', 'HEAD', 'GET'],
        'auth_user_register': ['POST'],
        'auth_user_login': ['POST'],
        'auth_refresh_token' : ['POST'],
        'job_applications' : ['GET'],
        'job_application': ['GET']
    }

    test = False

    @staticmethod
    def init_app(app):
        """Flask 애플리케이션에 AuthGuard를 초기화하는 메서드"""
        jwt.init_app(app)

        @jwt.token_in_blocklist_loader
        def check_if_token_revoked(jwt_header, jwt_payload):
            """토큰이 폐기되었는지 확인하는 콜백 함수"""
            token_type = jwt_payload.get("type", "access")  # 기본값으로 access
            jti = jwt_payload["jti"]
            db = next(get_db())

            if token_type == "access":
                # Access token의 경우 DB에서 추가 검증 없이 pass
                return False

            if token_type == "refresh":
                # Refresh token의 경우 DB에서 JTI를 검증
                token = get_login_by_user_id(db, jwt_payload["sub"])
                return token is None or token['login']['refresh_token'] != jti

            return True  # 알 수 없는 토큰 타입의 경우 기본적으로 거부

        
        @app.before_request
        def authenticate():
            print(request)
            print(request.endpoint)
            print(request.method)

            if request.endpoint is None:
                return

            if request.endpoint in AuthGuard.EXCLUDED_ENDPOINTS.keys():
                if request.method in AuthGuard.EXCLUDED_ENDPOINTS[request.endpoint]:
                    return

            if AuthGuard.test:
                g.middleware_executed = True
                return

            try:
                verify_jwt_in_request()
            except:
                return fail("인증 실패: JWT token is invalid!", 401)

            if 'Authorization' not in request.headers:
                return fail("인증 실패: JWT token is missing!", 401)

            @staticmethod
            def create_access_token(user_id, expires_delta=None):
                """액세스 토큰을 생성하는 메서드"""
                if expires_delta is None:
                    expires_delta = timedelta(minutes=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])

                current_time = now_korea()

                return create_access_token(
                    identity=user_id,
                    expires_delta=expires_delta,
                    additional_claims={
                        "type": "access",  # 토큰 타입 명시
                        "iat": current_time
                    }
                )

    @staticmethod
    def create_refresh_token(user_id, login_device_info=None, login_ip=None):
        """리프레시 토큰을 생성하고 데이터베이스에 저장하는 메서드"""
        expires_delta = current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        
        current_time = now_korea()
        expiration_time = current_time + expires_delta
        
        refresh_token = create_refresh_token(
            identity=user_id,
            expires_delta=expires_delta,
            additional_claims={"type": "refresh", "iat": current_time}
        )
        
        db = next(get_db())
        create_result = create_login(db, user_id, refresh_token, expiration_time, login_device_info, login_ip)
        
        if create_result['success']:
            return refresh_token
        else:
            print(f"Error creating refresh token in DB: {create_result['error']}")
            return None
