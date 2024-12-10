# services/bookmark_service.py
from flask import g

def register_bookmark(data):  # 함수 이름 수정: register_user -> register_bookmark
    """
    북마크 등록 테스트 함수
    """
    message = "register_bookmark 함수 실행됨"  # 메시지 수정
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed
    }

def get_bookmarks(query_params):  # 함수 이름 수정: get_application_log -> get_bookmarks
    """
    북마크 목록 가져오기 테스트 함수
    """
    message = "get_bookmarks 함수 실행됨"  # 메시지 수정
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed,
        "query_params": query_params  # 테스트용으로 받은 쿼리 파라미터 반환
    }