# services/job_service.py
from flask import g

def get_applications_list(query_params):
    """
    채용 공고 목록 가져오기 테스트 함수
    """
    message = "get_applications_list 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed,
        "query_params": query_params  # 테스트용으로 받은 쿼리 파라미터 반환
    }

def get_application(query_params):  # poster_id는 query_params에 포함될 것으로 예상
    """
    특정 채용 공고 가져오기 테스트 함수
    """
    message = "get_application 함수 실행됨"
    middleware_executed = g.get('middleware_executed', False)  # 미들웨어 실행 여부 확인
    return {
        "message": message,
        "middleware_executed": middleware_executed,
        "query_params": query_params  # 테스트용으로 받은 쿼리 파라미터 반환
    }