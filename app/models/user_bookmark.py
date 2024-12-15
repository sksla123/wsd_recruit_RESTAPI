# models/user_bookmark.py

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import and_

from . import Base

class UserBookmark(Base):
    """UserBookmark 테이블에 대한 SQLAlchemy 모델 클래스"""
    __tablename__ = "UserBookmark"

    user_id = Column(String(255), ForeignKey("User.user_id"), primary_key=True, nullable=False)
    poster_id = Column(String(255), ForeignKey("JobPosting.poster_id"), primary_key=True, nullable=False)

    # user = relationship("User", back_populates="bookmarks")
    # job_posting = relationship("JobPosting", back_populates="user_bookmarks")

    def to_dict(self):
        """UserBookmark 객체를 딕셔너리로 변환합니다."""
        return {
            "user_id": self.user_id,
            "poster_id": self.poster_id,
        }

def get_user_bookmarks(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """UserBookmark 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(UserBookmark).count()
    bookmarks = db.query(UserBookmark).offset(offset).limit(item_counts).all()
    return {
        "success": True,
        "user_bookmarks": [bookmark.to_dict() for bookmark in bookmarks],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_user_bookmark(db: Session, user_id: str, poster_id: str) -> dict:
    """새로운 UserBookmark를 생성하는 함수"""
    try:
        new_bookmark = UserBookmark(user_id=user_id, poster_id=poster_id)
        db.add(new_bookmark)
        db.commit()
        db.refresh(new_bookmark)
        return {"success": True, "user_bookmark": new_bookmark.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_user_bookmark_by_ids(db: Session, user_id_input: str, poster_id_input: str) -> dict:
    """user_id와 poster_id로 UserBookmark 정보를 가져오는 함수"""
    bookmark = db.query(UserBookmark).filter(and_(UserBookmark.user_id == user_id_input, UserBookmark.poster_id == poster_id_input)).first()
    if bookmark:
        return {"success": True, "user_bookmark": bookmark.to_dict()}
    else:
        return {"success": False, "message": "UserBookmark not found"}

def delete_user_bookmark(db: Session, user_id_input: str, poster_id_input: str) -> dict:
    """기존 UserBookmark 정보를 삭제하는 함수"""
    bookmark = db.query(UserBookmark).filter(and_(UserBookmark.user_id == user_id_input, UserBookmark.poster_id == poster_id_input)).first()
    if bookmark:
        try:
            db.delete(bookmark)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "UserBookmark not found"}