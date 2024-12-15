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
        tuple: (dict, str) - (결과 데이터, 메시지) 튜플
    """
    try:
        db = next(get_db())
        page = int(query_params.get('page', 1))
        per_page = 20

        # 정렬 기준
        sort_by = query_params.get('sort_by', 'last_updated_date')
        sort_order = query_params.get('sort_order', 'desc')
        sort_criteria = {sort_by: {'sorting_method': 0 if sort_order == 'asc' else 1}}

        # 필터링
        filters = []
        if 'location' in query_params:
            filters.append(JobPosting.loc_codes.contains(query_params['location']))
        if 'career' in query_params:
            filters.append(JobPosting.job_career == query_params['career'])
        if 'salary' in query_params:
            filters.append(JobPosting.sal_code == query_params['salary'])

        # 검색
        search_query = query_params.get('search', '')
        if search_query:
            filters.append(or_(
                JobPosting.poster_title.ilike(f'%{search_query}%'),
                JobPosting.job_sectors.ilike(f'%{search_query}%'),
                JobPosting.comp_id.ilike(f'%{search_query}%')  # 회사명 검색 (comp_id를 회사명으로 가정)
            ))

        result = get_available_job_postings_sorted_by(db, sort_criteria, page, per_page, filters)
        
        if result['success']:
            return result, "채용 공고 목록을 성공적으로 조회했습니다."
        else:
            return None, result['message']
    except Exception as e:
        return None, str(e)

def get_application(query_params, poster_id):
    """
    특정 채용 공고를 조회합니다.
    Args:
        query_params (dict): 쿼리 파라미터
        poster_id (int): 조회할 채용 공고 ID
    Returns:
        tuple: (dict, str) - (결과 데이터, 메시지) 튜플
    """
    try:
        db = next(get_db())
        result = get_job_posting_by_id(db, poster_id)
        if result['success']:
            return result['posting'], "채용 공고를 성공적으로 조회했습니다."
        else:
            return None, result['message']
    except Exception as e:
        return None, str(e)
