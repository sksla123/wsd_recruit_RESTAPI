# models/user_bookmark.py
from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class UserBookmark(Base):
    """
    UserBookmark 테이블 모델 (User와 JobPosting 간의 북마크 관계 연결 테이블)

    Attributes:
        user_id (str): 사용자 ID (FK, User 테이블 참조)
        poster_id (str): 공고 ID (FK, JobPosting 테이블 참조)
    """
    __tablename__ = 'UserBookmark'

    user_id = Column(String(255), ForeignKey('User.user_id'), primary_key=True, comment="사용자 ID")
    poster_id = Column(String(255), ForeignKey('JobPosting.poster_id'), primary_key=True, comment="공고 ID")

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'poster_id'),  # 복합 기본 키 설정
    )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "poster_id": self.poster_id
        }

def create_user_bookmark(db: Session, user_id: str, poster_id: str):
    """새로운 UserBookmark 레코드 생성"""
    try:
        db_user_bookmark = UserBookmark(user_id=user_id, poster_id=poster_id)
        db.add(db_user_bookmark)
        db.commit()
        db.refresh(db_user_bookmark)
        return db_user_bookmark.to_dict(), "북마크가 성공적으로 추가되었습니다."
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e):
            return None, "이미 북마크된 공고입니다."
        return None, f"데이터베이스 무결성 오류 (FK 제약 조건 위반): {str(e)}"
    except Exception as e:
        db.rollback()
        return None, f"북마크 추가 중 오류가 발생했습니다: {str(e)}"

def get_user_bookmark(db: Session, user_id: str, poster_id: str):
    """user_id와 poster_id로 UserBookmark 레코드 조회"""
    try:
        user_bookmark_obj = db.query(UserBookmark).filter(UserBookmark.user_id == user_id, UserBookmark.poster_id == poster_id).first()
        if user_bookmark_obj:
            return user_bookmark_obj.to_dict(), "북마크 조회 성공"
        return None, "해당하는 북마크가 없습니다."
    except Exception as e:
        return None, f"북마크 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_bookmark_list_by_user_id(db: Session, user_id: str):
    """user_id로 UserBookmark 레코드 목록 조회"""
    try:
        user_bookmark_list = db.query(UserBookmark).filter(UserBookmark.user_id == user_id).all()
        if user_bookmark_list:
            result = [user_bookmark.to_dict() for user_bookmark in user_bookmark_list]
            return result, f"해당 user_id({user_id})의 북마크 목록 조회 성공"
        return None, f"해당 user_id({user_id})의 북마크가 없습니다."
    except Exception as e:
        return None, f"북마크 목록 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_bookmark_list_by_poster_id(db: Session, poster_id: str):
    """poster_id로 UserBookmark 레코드 목록 조회 (어떤 사용자들이 이 공고를 북마크했는지)"""
    try:
        user_bookmark_list = db.query(UserBookmark).filter(UserBookmark.poster_id == poster_id).all()
        if user_bookmark_list:
            result = [user_bookmark.to_dict() for user_bookmark in user_bookmark_list]
            return result, f"해당 poster_id({poster_id})를 북마크한 사용자 목록 조회 성공"
        return None, f"해당 poster_id({poster_id})를 북마크한 사용자가 없습니다."
    except Exception as e:
        return None, f"북마크 목록 조회 중 오류가 발생했습니다: {str(e)}"


def delete_user_bookmark(db: Session, user_id: str, poster_id: str):
    """UserBookmark 레코드 삭제 (북마크 해제)"""
    try:
        user_bookmark_obj = db.query(UserBookmark).filter(UserBookmark.user_id == user_id, UserBookmark.poster_id == poster_id).first()
        if user_bookmark_obj:
            db.delete(user_bookmark_obj)
            db.commit()
            return None, "북마크가 성공적으로 해제되었습니다."
        return None, "해당하는 북마크가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"북마크 해제 중 오류가 발생했습니다: {str(e)}"

def delete_user_bookmark_by_user_id(db: Session, user_id: str):
    """user_id로 UserBookmark 레코드 일괄 삭제 (사용자의 모든 북마크 해제)"""
    try:
        delete_count = db.query(UserBookmark).filter(UserBookmark.user_id == user_id).delete()
        db.commit()
        return None, f"user_id({user_id})의 {delete_count}개 북마크가 해제되었습니다."
    except Exception as e:
        db.rollback()
        return None, f"사용자 북마크 일괄 해제 중 오류가 발생했습니다: {str(e)}"

def delete_user_bookmark_by_poster_id(db: Session, poster_id: str):
    """poster_id로 UserBookmark 레코드 일괄 삭제 (공고의 모든 북마크 해제)"""
    try:
        delete_count = db.query(UserBookmark).filter(UserBookmark.poster_id == poster_id).delete()
        db.commit()
        return None, f"poster_id({poster_id})의 {delete_count}개 북마크가 해제되었습니다."
    except Exception as e:
        db.rollback()
        return None, f"공고 북마크 일괄 해제 중 오류가 발생했습니다: {str(e)}"