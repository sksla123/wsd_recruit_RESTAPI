# services/bookmark_service.py
from ..models.database import get_db
from ..models.user_bookmark import create_user_bookmark, get_user_bookmark_by_ids, get_user_bookmarks

def register_bookmark(data, user_id):
    """
    북마크를 등록합니다.
    """
    try:
        db = next(get_db())
        poster_id = data.get('poster_id')

        if not user_id or not poster_id:
            return False, None, "사용자 ID와 포스터 ID는 필수입니다.", 400

        # 이미 존재하는 북마크인지 확인
        existing_bookmark = get_user_bookmark_by_ids(db, user_id, poster_id)
        if existing_bookmark['success']:
            return False, None, "이미 존재하는 북마크입니다.", 409

        # 새 북마크 생성
        result = create_user_bookmark(db, user_id, poster_id)
        if result['success']:
            return True, result['user_bookmark'], "북마크가 성공적으로 등록되었습니다.", 201
        else:
            return False, None, result['error'], 400
    except Exception as e:
        return False, None, str(e), 500

def get_bookmarks(user_id):
    """
    북마크 목록을 조회합니다.
    """
    try:
        db = next(get_db())
        result = get_user_bookmarks(db)
        if result['success']:
            # 현재 사용자의 북마크만 필터링
            user_bookmarks = [bm for bm in result['user_bookmarks'] if bm['user_id'] == user_id]
            return True, user_bookmarks, "북마크 목록을 성공적으로 조회했습니다.", 200
        else:
            return False, None, "북마크 목록 조회에 실패했습니다.", 400
    except Exception as e:
        return False, None, str(e), 500
