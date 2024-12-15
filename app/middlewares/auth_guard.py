import jwt
from flask import request, jsonify, current_app, g
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from ..views.response import JsonResponse, success, fail  # JsonResponse, success, fail 임포트

from ..models.database import db
from ..models.login import Login, get_login_by_user_id, create_login, delete_login # Models and database access functions import
from .. import db

class AuthGuard:
    EXCLUDED_ENDPOINTS = {
        'auth_user_register': ['POST'],
        'auth_refresh': ['POST']  # refresh token 요청 엔드포인트 추가
    }

    test = False

    @staticmethod
    def init_app(app):
        @app.before_request
        def authenticate():
            g.middleware_executed = False

            if request.endpoint in AuthGuard.EXCLUDED_ENDPOINTS.keys():
                if request.method in AuthGuard.EXCLUDED_ENDPOINTS[request.endpoint]:
                    return

            if AuthGuard.test:
                g.middleware_executed = True
                return

            # Authorization 헤더 확인
            token = request.headers.get('Authorization')
            if not token or not token.startswith("Bearer "):
                return JsonResponse(message="JWT token is missing or invalid!", status_code=401).to_response()

            # JWT 검증
            jwt_token = token.split(" ")[1]
            try:
                payload = AuthGuard.decode_token(jwt_token, app.config['JWT_SECRET_KEY'])
                request.user = payload  # 인증된 사용자 정보 저장

                # refresh token 검증 시 DB 확인 (refresh token 요청이 아닌 경우에만)
                if request.endpoint != 'auth_refresh': # refresh token 요청이 아닌 경우에만 검증
                    if payload.get('type') == 'refresh':
                        login_data = get_login_by_user_id(db.session, payload['user_id'])
                        if not login_data['success']:
                            return JsonResponse(message="Refresh token not found in database", status_code=401).to_response()
                        stored_refresh_token = login_data['login']['refresh_token']
                        if stored_refresh_token != jwt_token: # refresh token 정보 DB와 일치하지 않으면 오류
                            return JsonResponse(message="Invalid refresh token!", status_code=403).to_response()

            except jwt.ExpiredSignatureError:
                if payload.get('type') == 'refresh': # Refresh 토큰 만료 시 DB에서 삭제
                    login_data = get_login_by_user_id(db.session, payload['user_id'])
                    if login_data['success']:
                        delete_login(db.session, login_data['login']['refresh_id'])
                return JsonResponse(message="Token has expired!", status_code=401).to_response()

            except jwt.InvalidTokenError:
                return JsonResponse(message="Invalid token!", status_code=403).to_response()
            except Exception as e: # 기타 예외 처리
                return JsonResponse(message=f"Token verification failed: {str(e)}", status_code=500).to_response()


    @staticmethod
    def decode_token(token, secret_key):
        """
        JWT 디코딩 및 검증
        """
        return jwt.decode(token, secret_key, algorithms=["HS256"])

    @staticmethod
    def create_access_token(user_id, expires_in=None):
        """
        새로운 Access Token 생성
        """
        if expires_in is None:
            expires_in = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']

        # config에서 설정한 TIME_ZONE을 사용하여 한국 시간으로 설정
        time_zone = current_app.config['TIME_ZONE'] or "Asia/Seoul"
        current_time = datetime.now(ZoneInfo(time_zone))
        expiration_time = current_time + timedelta(minutes=expires_in)

        payload = {
            "user_id": user_id,
            "exp": expiration_time,
            "iat": current_time,
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")

    @staticmethod
    def create_refresh_token(user_id, login_device_info=None, login_ip=None):
        """
        Refresh Token 생성 및 DB 저장
        """
        expires_in = current_app.config['JWT_REFRESH_TOKEN_EXPIRES']

        # config에서 설정한 TIME_ZONE을 사용하여 한국 시간으로 설정
        time_zone = current_app.config['TIME_ZONE'] or "Asia/Seoul"
        current_time = datetime.now(ZoneInfo(time_zone))
        expiration_time = current_time + timedelta(minutes=expires_in)

        payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": expiration_time,
            "iat": current_time,
        }

        refresh_token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
        create_result = create_login(db.session, user_id, refresh_token, expiration_time, login_device_info, login_ip) # DB 저장

        if create_result['success']:
            return refresh_token
        else:
            print(f"Error creating refresh token in DB: {create_result['error']}") # 로깅 추가
            return None # DB 저장 실패 시 None 반환