# services/auth_service.py
from flask import g

def register_user(data):
    """
    회원 가입 테스트 함수
    """
    message = "register_user 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed
    }

def user_login(data):
    """
    로그인 테스트 함수
    """
    message = "user_login 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed
    }

def refresh_token(data):
    """
    토큰 갱신 테스트 함수
    """
    message = "refresh_token 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed
    }

def update_user_profile(data):
    """
    프로필 업데이트 테스트 함수
    """
    message = "update_user_profile 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed
    }