# services/job_service.py
from ..models.database import get_db
from ..models.job_posting import JobPosting, get_available_job_postings_sorted_by, get_job_posting_by_id
from sqlalchemy import or_

def get_applications_list(query_params):
    """
    채용 공고 목록을 조회합니다.
    Args:
        query_params (dict): 쿼리 파라미터
    Returns:
        tuple: (bool, dict, str, int) - 성공 여부, 결과 데이터, 메시지, HTTP 상태 코드
    """
    try:
        db = next(get_db())
        page = int(query_params.get('page', 1))
        per_page = 20

        # 정렬 기준 설정
        sort_by = query_params.get('sort_by', 'last_updated_date')  # 기본 정렬: last_updated_date
        sort_order = query_params.get('sort_order', 'desc')  # 기본 정렬 순서: 내림차순
        sort_criteria = {sort_by: {'sorting_method': 0 if sort_order == 'asc' else 1}}


        # 검색 조건 설정
        search_query = query_params.get('search', '')

        # 데이터베이스에서 채용 공고 조회
        result = get_available_job_postings_sorted_by(
            db=db,
            sort_criteria=sort_criteria,
            page=page,
            item_counts=per_page,
        )

        if result['success']:
            return True, result['postings'], "채용 공고 목록을 성공적으로 조회했습니다.", 200
        else:
            return False, None, result['message'], 400

    except Exception as e:
        return False, None, str(e), 500


def get_application(query_params, poster_id):
    """
    특정 채용 공고를 조회합니다.
    Args:
        query_params (dict): 쿼리 파라미터 (필요 시 사용)
        poster_id (int): 조회할 채용 공고 ID
    Returns:
        tuple: (bool, dict, str, int) - 성공 여부, 결과 데이터, 메시지, HTTP 상태 코드
    """
    try:
        db = next(get_db())
        
        # 특정 채용 공고 ID로 데이터 조회
        result = get_job_posting_by_id(db, poster_id)
        
        if result['success']:
            return True, result['posting'], "채용 공고를 성공적으로 조회했습니다.", 200
        else:
            return False, None, result['message'], 404

    except Exception as e:
        return False, None, str(e), 500
