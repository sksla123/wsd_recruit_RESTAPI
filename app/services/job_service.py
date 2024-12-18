# services/job_service.py
from ..models.database import get_db
from ..models.job_posting import JobPosting, get_available_job_postings, get_job_posting_by_id, increment_view_count
from datetime import datetime
from sqlalchemy import or_

# 필터 조건 정의
AVAILABLE_FILTERS = {
    "title_contains": str,
    "comp_id": int,
    "sal_code_eq": int,
    "sal_code_gte": int, 
    "sal_code_lte": int, 
    "edu_code_eq": int,
    "edu_code_gte": int,
    "edu_code_lte": int, 
    "deadline_date_eq": str,
    "deadline_date_gte": str, 
    "deadline_date_lte": str, 
    "loc_codes": int,  # 리스트 내 포함 여부 검사
    "job_codes": int,  # 리스트 내 포함 여부 검사
}

def validate_filters(filters: dict) -> dict:
    """
    주어진 필터의 유효성을 검사.
    :param filters: 사용자 입력 필터
    :return: {"success": bool, "invalid_keys": list, "message": str}
    """
    invalid_keys = []
    
    for key, value in filters.items():
        if key not in AVAILABLE_FILTERS:
            invalid_keys.append(key)
            continue

        expected_format = AVAILABLE_FILTERS[key]
        
        # 리스트 처리 (loc_codes, job_codes)
        if isinstance(value, list):
            if not all(isinstance(v, int) for v in value):
                invalid_keys.append(key)
                continue

        # 복합 조건 처리 (e.g., eq, gte, lte, contains)
        elif isinstance(expected_format, dict):
            if not isinstance(value, dict):
                invalid_keys.append(key)
                continue
            for op, val in value.items():
                if op not in expected_format or not isinstance(val, expected_format[op]):
                    invalid_keys.append(f"{key}.{op}")
                    break

        # 단일 조건 처리 (e.g., title_contains, comp_id)
        elif not isinstance(value, expected_format):
            invalid_keys.append(key)

        # 추가적으로 날짜 포맷 검증 (deadline_date 같은 경우)
        if key == "deadline_date" and isinstance(value, dict):
            for op, date_str in value.items():
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    invalid_keys.append(f"{key}.{op}")
    
    if invalid_keys:
        return {
            "success": False,
            "invalid_keys": invalid_keys,
            "message": f"Invalid filter keys or values: {', '.join(invalid_keys)}"
        }
    
    return {"success": True, "message": "All filters are valid"}


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
        sort_by = query_params.get('sort_by', 'deadline_date')  # 기본 정렬: deadline_date
        if sort_by not in ['deadline_date']:
            return False, None, "Not valid sort option.", 400

        sort_order = query_params.get('sort_order', 'asc')  # 정렬 순서: 내림차순('desc') 1, 오름차순('asc') 0
        sort_criteria = {sort_by: {'sorting_method': 0 if sort_order == 'asc' else 1}}

        # 필터링 조건 설정 (query_params에서 바로 추출)
        filters = {}
        for key, value in query_params.items():
            if key in AVAILABLE_FILTERS:
                expected_type = AVAILABLE_FILTERS[key]

                # 리스트 처리 (loc_codes, job_codes)
                if isinstance(expected_type, int) and isinstance(value, str) and ',' in value:
                    filters[key] = [int(v) for v in value.split(',')]  # 예: "loc_codes=1,2,3"
                else:
                    # 기본적으로 문자열을 적절한 타입으로 변환
                    if expected_type == int:
                        filters[key] = int(value)
                    elif expected_type == str:
                        filters[key] = value
                    else:
                        filters[key] = value  # 다른 경우 처리 (예: 날짜나 복합 조건)

        # 필터 유효성 검사
        validation_result = validate_filters(filters)
        if not validation_result['success']:
            return False, None, validation_result['message'], 400

        # 데이터베이스에서 채용 공고 조회
        result = get_available_job_postings(
            db=db,
            sort_criteria=sort_criteria,
            page=page,
            item_counts=per_page,
            filters=filters,
        )

        if result['success']:
            return True, result['postings'], "채용 공고 목록을 성공적으로 조회했습니다.", 200
        else:
            return False, None, result['message'], 400

    except Exception as e:
        return False, None, str(e), 500

def get_application(query_params, poster_id):
    """
    특정 채용 공고를 조회하고, 조회할 때 view_cnts 값을 1 증가시킵니다.
    Args:
        query_params (dict): 쿼리 파라미터 (필요 시 사용)
        poster_id (int): 조회할 채용 공고 ID
    Returns:
        tuple: (bool, dict, str, int) - 성공 여부, 결과 데이터, 메시지, HTTP 상태 코드
    """
    try:
        db = next(get_db())
        
        # view_cnts 값을 1 증가
        increment_result = increment_view_count(db, poster_id)
        
        if not increment_result['success']:
            return False, None, increment_result['message'], 500
        
        # 특정 채용 공고 ID로 데이터 조회
        result = get_job_posting_by_id(db, poster_id)
        
        if result['success']:
            return True, result['posting'], "채용 공고를 성공적으로 조회했습니다.", 200
        else:
            return False, None, result['message'], 404

    except Exception as e:
        return False, None, str(e), 500
