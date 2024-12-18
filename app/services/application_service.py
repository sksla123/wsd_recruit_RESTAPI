# services/application_service.py
from flask import g
from ..models.database import get_db
from ..models.user_applicated import create_user_applicated, ApplicationStatus, get_user_applicated_by_id, update_user_applicated
from ..models.user_applicated_log import create_user_applicated_log, get_user_applicated_log_by_user_id, ApplicateAction

def applicate(data):
    """
    지원하기 테스트 함수
    """
    try:
        db = next(get_db())
        user_id = data.get('user_id')
        poster_id = data.get('poster_id')
        application = data.get('application')
        
        result = create_user_applicated(db, user_id, poster_id, application, ApplicationStatus.APPLIED)
        
        if result['success']:
            log_result = create_user_applicated_log(db, result['user_applicated']['application_id'], user_id, poster_id, ApplicateAction.CREATE)
            if not log_result['success']:
                return False, None, "Failed to create application log", 500
            
            return True, result['user_applicated'], "Application submitted successfully", 201
        else:
            return False, None, "Failed to submit application", 400
    except Exception as e:
        return False, None, str(e), 500

def get_application_log(query_params, current_user):
    """
    지원 로그 가져오기 테스트 함수
    """
    try:
        db = next(get_db())
        
        result = get_user_applicated_log_by_user_id(db, current_user)
        print(result)
        
        if result['success']:
            return True, result, "Application logs retrieved successfully", 200
        else:
            return False, None, "Failed to retrieve application logs", 400
    except Exception as e:
        return False, None, str(e), 500

def update_application_status(data, application_id, current_user):
    """
    지원 상태 업데이트 테스트 함수
    """
    try:
        db = next(get_db())
        new_status = ApplicationStatus(data.get('new_status'))

        if new_status is None:
            return False, None, "필수적인 키가 제공되지 않음", 400
        
        if new_status.value not in [ApplicationStatus.APPLIED.value, ApplicationStatus.CANCELLED.value]:
            return False, None, "허용되지 않은 동작입니다.", 409

        applicated = get_user_applicated_by_id(db, application_id)

        if not applicated['success']:
            return False, None, "Application not found", 404
        
        # 현재 사용자와 지원서의 user_id 비교
        if applicated['user_applicated']['user_id'] != current_user:
            return False, None, "권한이 없습니다. 본인의 지원서만 수정할 수 있습니다.", 403
        
        result = update_user_applicated(db, application_id, new_application_status=new_status.value)

        if result['success']:
            log_result = create_user_applicated_log(db, application_id, result['user_applicated']['user_id'], 
                                                    result['user_applicated']['poster_id'], ApplicateAction.UPDATE.value)
            if not log_result['success']:
                return False, None, "Failed to create update log", 500
            
            return True, result['user_applicated'], "Application status updated successfully", 200
        else:
            return False, None, "Failed to update application status", 400
    except Exception as e:
        return False, None, str(e), 500
