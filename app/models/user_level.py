# models/user_level.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from . import Base

class UserLevel(Base):
    """
    UserLevel 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "UserLevel"

    user_level = Column(Integer, primary_key=True)  # 변경됨
    user_level_name = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "user_level": self.user_level,  # 변경됨
            "user_level_name": self.user_level_name
        }

def get_user_levels(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """UserLevel 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    user_levels = db.query(UserLevel).offset(offset).limit(item_counts).all()
    total_count = db.query(UserLevel).count()
    return {
        "user_levels": [user_level.to_dict() for user_level in user_levels],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_user_level(db: Session, level: int, level_name: str) -> dict: #인자명 변경
    """새로운 UserLevel을 생성하는 함수"""
    try:
        new_user_level = UserLevel(user_level=level, user_level_name=level_name) # 변경됨
        db.add(new_user_level)
        db.commit()
        db.refresh(new_user_level)
        return {"success": True, "user_level": new_user_level.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_user_level_by_id(db: Session, level_id: int) -> dict: # 인자명 변경
    """level로 UserLevel 정보를 가져오는 함수"""
    user_level = db.query(UserLevel).filter(UserLevel.user_level == level_id).first() # 변경됨
    if user_level:
        return {"success": True, "user_level": user_level.to_dict()}
    else:
        return {"success": False, "message": "UserLevel not found"}

def update_user_level(db: Session, level_id: int, new_level_name: str) -> dict: # 인자명 변경
    """기존 UserLevel 정보를 수정하는 함수"""
    user_level = db.query(UserLevel).filter(UserLevel.user_level == level_id).first() # 변경됨
    if user_level:
        try:
            user_level.user_level_name = new_level_name
            db.commit()
            return {"success": True, "user_level": user_level.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "UserLevel not found"}

def delete_user_level(db: Session, level_id: int) -> dict: # 인자명 변경
    """기존 UserLevel 정보를 삭제하는 함수"""
    user_level = db.query(UserLevel).filter(UserLevel.user_level == level_id).first() # 변경됨
    if user_level:
        try:
            db.delete(user_level)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "UserLevel not found"}