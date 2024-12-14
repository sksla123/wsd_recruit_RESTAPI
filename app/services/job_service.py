# services/job_service.py
from flask import g

def get_applications_list(query_params):
    """
    채용 공고 목록을 조회합니다.

    Args:
        query_params (dict): 쿼리 파라미터

    Returns:
        tuple: (dict, str) - (결과 데이터, 메시지) 튜플
    """
    message = "get_applications_list 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)
    return {
        "middleware_executed": middleware_executed,
        "query_params": query_params
    }, message

def get_application(query_params, poster_id):
    """
    특정 채용 공고를 조회합니다.

    Args:
        query_params (dict): 쿼리 파라미터
        poster_id (int): 조회할 채용 공고 ID

    Returns:
        tuple: (dict, str) - (결과 데이터, 메시지) 튜플
    """
    message = f"get_application 함수 실행됨 (poster_id: {poster_id})" # 메시지에 poster_id 추가
    middleware_executed = g.get('middleware_executed', False)
    return {
        "middleware_executed": middleware_executed,
        "query_params": query_params,
        "poster_id": poster_id #반환 데이터에 poster_id 포함
    }, message