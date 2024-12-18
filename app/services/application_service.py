# services/application_service.py
from flask import g
from ..models.database import get_db
from ..models.user_applicated import create_user_applicated, ApplicationStatus, get_user_applications_by_user_id, delete_user_applicated, get_user_applicated_by_id, get_user_applicated_by_ids, update_user_applicated
from ..models.user_applicated_log import create_user_applicated_log, get_user_applicated_log_by_user_id, ApplicateAction
from ..models.user import get_user_by_id

def applicate(data, current_user):
    """
    지원하기 함수
    """
    try:
        db = next(get_db())
        user_id = current_user
        poster_id = data.get('poster_id')
        application = data.get('application')
        
        # 기존 제출 내용 확인
        existing_application = get_user_applicated_by_ids(db, user_id, poster_id)
        if existing_application['success']:
            return False, existing_application['user_applicated'], "Application already exists for this user and poster, Use PUT method to update", 400
        
        result = create_user_applicated(db, user_id, poster_id, application, ApplicationStatus.APPLIED)
        
        if result['success']:
            log_result = create_user_applicated_log(db, result['user_applicated']['application_id'], user_id, poster_id, ApplicateAction.CREATE)
            if not log_result['success']:
                return False, None, "Failed to create application log", 500
            
            return True, result.get('user_applicated'), "Application submitted successfully", 201
        else:
            return False, None, "Failed to submit application", 400
    except Exception as e:
        return False, None, str(e), 500
    
def update_application(data, current_user):
    """
    지원서 변경 함수
    """
    try:
        db = next(get_db())
        user_id = current_user
        application_id = data.get('application_id')
        action = data.get('action')
        new_value = data.get('new_value')

        if action is None or new_value is None or application_id is None:
            return False, None, "Not enough datas. It needs action and new_value for update", 400
        
        new_application = None
        new_application_status = None

        if action == 'application':
            new_application = new_value
        # elif action == 'application_status':
        #     try:
        #         new_value = int(new_value)
        #     except:
        #         return False, None, "application status must be Integer", 400
        #     if new_value not in range(4):
        #         return False, None, "application status must be in range(0~3)", 400
        #     new_application_status = new_value
        else:
            return False, None, "Action must be one of ['application']", 400
        
        # 기존 제출 내용 확인
        existing_application = get_user_applicated_by_id(db, application_id)
        if not existing_application['success']:
            return False, None, "지원서를 찾을 수 없습니다.", 400
        # print(existing_application)
                
        application_to_update = existing_application['user_applicated']
        # {
        #     "application_id": self.application_id,
        #     "user_id": self.user_id,
        #     "poster_id": self.poster_id,
        #     "application": self.application,
        #     "application_status": self.application_status,
        # }

        if application_to_update["user_id"] != user_id:
            return False, None, "Unauthorized User", 404
        if application_to_update[action] == new_value:
            return False, None, "Data is not updated. (New value is same as before)", 400

        result = update_user_applicated(db, application_id, new_application, new_application_status)
        
        if result['success']:
            log_result = create_user_applicated_log(db, result['user_applicated']['application_id'], user_id, application_to_update['poster_id'], ApplicateAction.UPDATE.value)
            if not log_result['success']:
                return False, None, "Failed to create application log(Though, application is updated)", 500
            
            return True, result['user_applicated'], "Application updated successfully", 201
        else:
            return False, None, "Failed to update application", 400
    except Exception as e:
        return False, None, str(e), 500

def get_application_log(query_params, current_user):
    """
    지원 로그 가져오기 함수
    """
    try:
        db = next(get_db())
        page = int(query_params.get('page', '1'))

        result = get_user_applicated_log_by_user_id(db, current_user, page)
        print(result)
        
        if result['success']:
            return True, result['data'], "Application logs retrieved successfully", 200
        else:
            return False, None, "Failed to retrieve application logs", 400
    except Exception as e:
        return False, None, str(e), 500

def cancel_application_status(application_id, current_user):
    """
    지원 상태 업데이트 함수
    """
    try:
        db = next(get_db())

        applicated = get_user_applicated_by_id(db, application_id)

        if not applicated['success']:
            return False, None, "Application not found", 404
        
        # 현재 사용자와 지원서의 user_id 비교
        if applicated['user_applicated']['user_id'] != current_user:
            return False, None, "권한이 없습니다. 본인의 지원서만 수정할 수 있습니다.", 403
        
        poster_id=applicated['user_applicated']['poster_id']
        log_result = create_user_applicated_log(db, application_id, current_user, 
                                                poster_id, ApplicateAction.DELETE.value)
        if not log_result['success']:
            return False, None, "Failed to create update log, not successfully deleted.", 500
        
        result = delete_user_applicated(db, application_id)

        if result['success']:    
            return True, applicated['user_applicated'], "Application canceled successfully", 200
        else:
            return False, None, "Failed to update application status", 400
    except Exception as e:
        return False, None, str(e), 500
    
def get_user_applications(data, current_user):
    """
    지원서를 가져오는는 함수
    """
    try:
        db = next(get_db())
        page = int(data.get("page", "1"))

        result = get_user_applications_by_user_id(db, current_user, page)

        if result['success']:
            return True, result['data'], "Application list is loaded successfully", 200
        else:
            return False, None, "Failed to load application list", 400
    except Exception as e:
        return False, None, str(e), 500
