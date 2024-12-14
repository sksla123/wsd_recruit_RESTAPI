# services/bookmark_service.py
from flask import g

def register_bookmark(data):
    """
    북마크를 등록합니다.

    Args:
        data (dict): 북마크 정보가 담긴 딕셔너리

    Returns:
        tuple: (dict: 결과 데이터, str: 메시지) 형태의 튜플
    """
    message = "register_bookmark 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "middleware_executed": middleware_executed,
        "input_data": data #입력 받은 데이터도 함께 반환
    }, message

def get_bookmarks(query_params):
    """
    북마크 목록을 조회합니다.

    Args:
        query_params (dict): 쿼리 파라미터

    Returns:
        tuple: (dict: 결과 데이터, str: 메시지) 형태의 튜플
    """
    message = "get_bookmarks 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "middleware_executed": middleware_executed,
        "query_params": query_params
    }, message