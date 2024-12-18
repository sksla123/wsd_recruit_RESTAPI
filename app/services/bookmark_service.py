# services/bookmark_service.py
from ..models.database import get_db
from ..models.user_bookmark import create_user_bookmark, get_user_bookmark_by_ids, get_user_bookmark_by_user_id, delete_user_bookmark

def toggle_bookmark(user_id, poster_id):
    """
    해당 포스터를 북마크 등록/ 해제 합니다.
    """
    try:
        success, data, message, status = register_bookmark(user_id, poster_id)
        if success:
            return success, {}, message, status 
        if message == "이미 존재하는 북마크입니다.":
            db = next(get_db())
            result = delete_user_bookmark(db, user_id, poster_id)
            if result['success']:
                return True, {}, "북마크가 해제되었습니다.", 200
        raise Exception
    except Exception as e:
        return False, None, "Unknown Error is occured while toggling bookmark", 500

def register_bookmark(user_id, poster_id):
    """
    북마크를 등록합니다.
    """
    try:
        db = next(get_db())

        if not user_id or not poster_id:
            return False, None, "사용자 ID와 포스터 ID는 필수입니다.", 400
        # print("a")
        # 이미 존재하는 북마크인지 확인
        existing_bookmark = get_user_bookmark_by_ids(db, user_id, poster_id)
        if existing_bookmark['success']:
            return False, None, "이미 존재하는 북마크입니다.", 409
        
        # 새 북마크 생성
        result = create_user_bookmark(db, user_id, poster_id)
        print(result)
        if result['success']:
            return True, result['user_bookmark'], "북마크가 성공적으로 등록되었습니다.", 201
        else:
            return False, None, result['error'], 400
    except Exception as e:
        return False, None, str(e), 500

def get_bookmarks(data, user_id):
    """
    북마크 목록을 조회합니다.
    """
    try:
        db = next(get_db())
        page = int(data.get('page', '1'))
        result = get_user_bookmark_by_user_id(db, user_id, page)
        print(result)
        if result['message'] == "UserBookmark not found" or result['success']:
            return True, result['data'], "북마크 목록을 성공적으로 조회했습니다.", 200
        else:
            return False, None, result['message'], 400
    except Exception as e:
        return False, None, str(e), 500
