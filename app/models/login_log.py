# models/login_log.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, relationship, Session
from datetime import datetime

from . import Base

class LoginLog(Base):
    """LoginLog 테이블에 대한 SQLAlchemy 모델 클래스"""
    __tablename__ = "LoginLog"

    login_log_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    login_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    login_id = Column(String(255), ForeignKey("User.user_id"), nullable=False)
    login_ip = Column(String(255))
    login_device_info = Column(Text)
    login_success = Column(Integer) # 성공 1, 실패 0으로 저장

    # user = relationship("User", back_populates="login_logs")

    def to_dict(self):
        """LoginLog 객체를 딕셔너리로 변환합니다."""
        return {
            "login_log_id": self.login_log_id,
            "login_date": self.login_date.isoformat() if self.login_date else None,  # ISO format으로 변환
            "login_id": self.login_id,
            "login_ip": self.login_ip,
            "login_device_info": self.login_device_info,
            "login_success": self.login_success
        }

def get_login_logs(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """LoginLog 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(LoginLog).count()
    login_logs = db.query(LoginLog).order_by(LoginLog.login_date.desc()).offset(offset).limit(item_counts).all() #최신 순으로 정렬 추가
    return {
        "success": True,
        "login_logs": [log.to_dict() for log in login_logs],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_login_log(db: Session, login_id: str, login_ip: str = None, login_device_info: str = None, login_success: int = 0) -> dict:
    """새로운 LoginLog 정보를 생성하는 함수"""
    try:
        new_log = LoginLog(login_id=login_id, login_ip=login_ip, login_device_info=login_device_info, login_success=login_success)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return {"success": True, "login_log": new_log.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_login_log_by_id(db: Session, login_log_id_input: int) -> dict:
    """login_log_id로 LoginLog 정보를 가져오는 함수"""
    log = db.query(LoginLog).filter(LoginLog.login_log_id == login_log_id_input).first()
    if log:
        return {"success": True, "login_log": log.to_dict()}
    else:
        return {"success": False, "message": "LoginLog not found"}

def delete_login_log(db: Session, login_log_id_input: int) -> dict:
    """기존 LoginLog 정보를 삭제하는 함수"""
    log = db.query(LoginLog).filter(LoginLog.login_log_id == login_log_id_input).first()
    if log:
        try:
            db.delete(log)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "LoginLog not found"}

def get_login_logs_by_login_id(db: Session, login_id_input: str, page: int = 1, item_counts: int = 20) -> dict:
    """login_id로 LoginLog 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(LoginLog).filter(LoginLog.login_id == login_id_input).count()
    login_logs = db.query(LoginLog).filter(LoginLog.login_id == login_id_input).order_by(LoginLog.login_date.desc()).offset(offset).limit(item_counts).all() #최신 순으로 정렬 추가
    return {
        "success": True,
        "login_logs": [log.to_dict() for log in login_logs],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }