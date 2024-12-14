import jwt
from flask import request, jsonify, current_app, g
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class AuthGuard:
    EXCLUDED_ENDPOINTS = {
        'auth_user_register': ['POST']
    }

    test = True

    @staticmethod
    def init_app(app):
        @app.before_request
        def authenticate():
            g.middleware_executed = False 

            if request.endpoint in AuthGuard.EXCLUDED_ENDPOINTS.keys():
                if  request.method in AuthGuard.EXCLUDED_ENDPOINTS[request.endpoint]:
                    return

            
            if AuthGuard.test: 
                g.middleware_executed = True
                return
            
            # Authorization 헤더 확인
            token = request.headers.get('Authorization')
            if not token or not token.startswith("Bearer "):
                return jsonify({"message": "JWT token is missing or invalid!"}), 401

            # JWT 검증
            jwt_token = token.split(" ")[1]
            try:
                payload = AuthGuard.decode_token(jwt_token, app.config['JWT_SECRET_KEY'])
                request.user = payload  # 인증된 사용자 정보 저장
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired!"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token!"}), 403

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
        time_zone = current_app.config['TIME_ZONE'] or "Asia/Seoul"  # 환경 변수로 설정된 타임존을 사용, 없으면 기본값으로 "Asia/Seoul" 사용
        current_time = datetime.now(ZoneInfo(time_zone))  # 환경 변수의 타임존으로 현재 시간 가져오기
        expiration_time = current_time + timedelta(minutes=expires_in)

        payload = {
            "user_id": user_id,
            "exp": expiration_time,  # 타임존 적용된 만료 시간 설정
            "iat": current_time,     # 타임존 적용된 발급 시간 설정
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")

    @staticmethod
    def create_refresh_token(user_id):
        """
        Refresh Token 생성 (DB에 저장 필요)
        """
        expires_in = current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        
        # config에서 설정한 TIME_ZONE을 사용하여 한국 시간으로 설정
        time_zone = current_app.config['TIME_ZONE'] or "Asia/Seoul"  # 환경 변수로 설정된 타임존을 사용, 없으면 기본값으로 "Asia/Seoul" 사용
        current_time = datetime.now(ZoneInfo(time_zone))  # 환경 변수의 타임존으로 현재 시간 가져오기
        expiration_time = current_time + timedelta(minutes=expires_in)

        payload = {
            "user_id": user_id,
            "type": "refresh",  # Refresh Token을 구분하기 위한 타입
            "exp": expiration_time,  # 타임존 적용된 만료 시간 설정
            "iat": current_time,     # 타임존 적용된 발급 시간 설정
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm="HS256")
