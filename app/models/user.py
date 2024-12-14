# models/user.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
from datetime import datetime

Base = declarative_base()

class User(Base):
    """
    User 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "User"

    user_id = Column(String(255), primary_key=True)
    user_email = Column(String(255), nullable=False)
    user_level = Column(Integer, ForeignKey("UserLevel.user_level"))
    user_password = Column(String(255), nullable=False)
    created_date = Column(DateTime, nullable=False)
    last_updated_date = Column(DateTime, nullable=False)
    user_bookmark = Column(JSON)
    user_applicated = Column(JSON)

    level = relationship("UserLevel", back_populates="users")

    def to_dict(self):
        """
        User 객체를 딕셔너리로 변환합니다.
        """
        return {
            "user_id": self.user_id,
            "user_email": self.user_email,
            "user_level": self.user_level,
            "user_password": self.user_password, #보안상 반환하지 않는 것이 좋습니다.
            "created_date": self.created_date.isoformat(),
            "last_updated_date": self.last_updated_date.isoformat(),
            "user_bookmark": self.user_bookmark,
            "user_applicated": self.user_applicated,
        }

def get_users(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """
    User 목록을 조회하는 함수 (Pagination 적용)
    """
    offset = (page - 1) * item_counts
    users = db.query(User).offset(offset).limit(item_counts).all()
    total_count = db.query(User).count()
    return {
        "users": [user.to_dict() for user in users],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_user(db: Session, user_id: str, user_email: str, user_password: str, user_level: int=None, user_bookmark: dict=None, user_applicated: dict=None) -> dict:
    """
    새로운 User를 생성하는 함수
    """
    try:
        now = datetime.now()
        new_user = User(user_id=user_id, user_email=user_email, user_password=user_password, user_level=user_level, created_date=now, last_updated_date=now, user_bookmark=user_bookmark, user_applicated=user_applicated)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"success": True, "user": new_user.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_user_by_id(db: Session, user_id_input: str) -> dict:
    """
    user_id로 User 정보를 가져오는 함수
    """
    user = db.query(User).filter(User.user_id == user_id_input).first()
    if user:
        return {"success": True, "user": user.to_dict()}
    else:
        return {"success": False, "message": "User not found"}

def update_user(db: Session, user_id_input: str, new_user_email: str = None, new_user_password: str = None, new_user_level: int = None, new_user_bookmark: dict = None, new_user_applicated: dict = None) -> dict:
    """
    기존 User 정보를 수정하는 함수
    """
    user = db.query(User).filter(User.user_id == user_id_input).first()
    if user:
        try:
            if new_user_email is not None: user.user_email = new_user_email
            if new_user_password is not None: user.user_password = new_user_password
            if new_user_level is not None: user.user_level = new_user_level
            if new_user_bookmark is not None: user.user_bookmark = new_user_bookmark
            if new_user_applicated is not None: user.user_applicated = new_user_applicated
            user.last_updated_date = datetime.now()
            db.commit()
            return {"success": True, "user": user.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "User not found"}

def delete_user(db: Session, user_id_input: str) -> dict:
    """
    기존 User 정보를 삭제하는 함수
    """
    user = db.query(User).filter(User.user_id == user_id_input).first()
    if user:
        try:
            db.delete(user)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "User not found"}