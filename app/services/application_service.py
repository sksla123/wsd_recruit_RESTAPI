# services/application_service.py
from flask import g

def applicate(data):
    """
    지원하기 테스트 함수
    """
    message = "applicate 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed
    }

def get_application_log(query_params):
    """
    지원 로그 가져오기 테스트 함수
    """
    message = "get_application_log 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed,
        "query_params": query_params  # 테스트용으로 받은 쿼리 파라미터 반환
    }

def update_application_status(data, application_id):
    """
    지원 상태 업데이트 테스트 함수
    """
    message = "update_application_status 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed,
        "application_id": application_id  # 테스트용으로 받은 application_id 반환
    }