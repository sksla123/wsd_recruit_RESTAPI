# models/login.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, relationship, Session
from datetime import datetime

from . import Base

class Login(Base):
    """Login 테이블에 대한 SQLAlchemy 모델 클래스"""
    __tablename__ = "Login"

    refresh_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String(255), ForeignKey("User.user_id"), nullable=False)
    refresh_token = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    login_device_info = Column(Text)
    login_ip = Column(String(255))

    # user = relationship("User", back_populates="logins")

    def to_dict(self):
        """Login 객체를 딕셔너리로 변환합니다."""
        return {
            "refresh_id": self.refresh_id,
            "user_id": self.user_id,
            "refresh_token": self.refresh_token,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "login_device_info": self.login_device_info,
            "login_ip": self.login_ip
        }

def get_logins(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """Login 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(Login).count()
    logins = db.query(Login).offset(offset).limit(item_counts).all()
    return {
        "success": True,
        "logins": [login.to_dict() for login in logins],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_login(db: Session, user_id: str, refresh_token: str, expires_at: datetime, login_device_info: str = None, login_ip: str = None) -> dict:
    """새로운 Login 정보를 생성하는 함수"""
    try:
        new_login = Login(user_id=user_id, refresh_token=refresh_token, expires_at=expires_at, login_device_info=login_device_info, login_ip=login_ip)
        db.add(new_login)
        db.commit()
        db.refresh(new_login)
        return {"success": True, "login": new_login.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_login_by_refresh_id(db: Session, refresh_id_input: int) -> dict:
    """refresh_id로 Login 정보를 가져오는 함수"""
    login = db.query(Login).filter(Login.refresh_id == refresh_id_input).first()
    if login:
        return {"success": True, "login": login.to_dict()}
    else:
        return {"success": False, "message": "Login not found"}
    
def get_login_by_refresh_token(db: Session, refresh_token_input: str) -> dict:
    """refresh_id로 Login 정보를 가져오는 함수"""
    login = db.query(Login).filter(Login.refresh_token == refresh_token_input).first()
    if login:
        return {"success": True, "login": login.to_dict()}
    else:
        return {"success": False, "message": "Login not found"}

def delete_login(db: Session, refresh_id_input: int) -> dict:
    """기존 Login 정보를 삭제하는 함수"""
    login = db.query(Login).filter(Login.refresh_id == refresh_id_input).first()
    if login:
        try:
            db.delete(login)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "Login not found"}
    
def delete_login_by_refresh_token(db: Session, refresh_token_input: str) -> dict:
    """기존 Login 정보를 삭제하는 함수"""
    login = db.query(Login).filter(Login.refresh_token == refresh_token_input).first()

    if login:
        try:
            db.delete(login)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "Login not found"}

def get_login_by_user_id(db: Session, user_id_input: str) -> dict:
    """user_id로 Login 정보를 가져오는 함수"""
    login = db.query(Login).filter(Login.user_id == user_id_input).first()
    if login:
        return {"success": True, "login": login.to_dict()}
    else:
        return {"success": False, "message": "Login not found"}