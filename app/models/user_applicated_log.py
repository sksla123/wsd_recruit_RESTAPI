# models/user_applicated_log.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, Session
from datetime import datetime
from sqlalchemy import and_

Base = declarative_base()

class ApplicateAction(enum.Enum):
    CREATE = 0 # 생성
    UPDATE = 1 # 수정
    DELETE = 2 # 삭제

class UserApplicatedLog(Base):
    """UserApplicatedLog 테이블에 대한 SQLAlchemy 모델 클래스"""
    __tablename__ = "UserApplicatedLog"

    application_log_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    application_id = Column(Integer, ForeignKey("UserApplicated.application_id"), nullable=False)
    applicated_at = Column(DateTime, nullable=False, default=datetime.utcnow) #default 추가
    user_id = Column(String(255), ForeignKey("User.user_id"), nullable=False)
    poster_id = Column(String(255), ForeignKey("JobPosting.poster_id"), nullable=False)
    applicate_action = Column(ENUM(ApplicateAction), nullable=False)

    user_applicated = relationship("UserApplicated", back_populates="logs")
    user = relationship("User", back_populates="applicated_logs")
    job_posting = relationship("JobPosting", back_populates="applicated_logs")
    

    def to_dict(self):
        """UserApplicatedLog 객체를 딕셔너리로 변환합니다."""
        return {
            "application_log_id": self.application_log_id,
            "application_id": self.application_id,
            "applicated_at": self.applicated_at.isoformat() if self.applicated_at else None, # DateTime 직렬화 처리 추가
            "user_id": self.user_id,
            "poster_id": self.poster_id,
            "applicate_action": self.applicate_action.value if self.applicate_action else None
        }

def get_user_applicated_logs(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """UserApplicatedLog 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(UserApplicatedLog).count()
    logs = db.query(UserApplicatedLog).offset(offset).limit(item_counts).all()
    return {
        "success": True,
        "user_applicated_logs": [log.to_dict() for log in logs],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_user_applicated_log(db: Session, application_id: int, user_id: str, poster_id: str, applicate_action: ApplicateAction) -> dict:
    """새로운 UserApplicatedLog를 생성하는 함수"""
    try:
        new_log = UserApplicatedLog(application_id=application_id, user_id=user_id, poster_id=poster_id, applicate_action=applicate_action)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return {"success": True, "user_applicated_log": new_log.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_user_applicated_log_by_id(db: Session, application_log_id_input: int) -> dict:
    """application_log_id로 UserApplicatedLog 정보를 가져오는 함수"""
    log = db.query(UserApplicatedLog).filter(UserApplicatedLog.application_log_id == application_log_id_input).first()
    if log:
        return {"success": True, "user_applicated_log": log.to_dict()}
    else:
        return {"success": False, "message": "UserApplicatedLog not found"}

def delete_user_applicated_log(db: Session, application_log_id_input: int) -> dict:
    """기존 UserApplicatedLog 정보를 삭제하는 함수"""
    log = db.query(UserApplicatedLog).filter(UserApplicatedLog.application_log_id == application_log_id_input).first()
    if log:
        try:
            db.delete(log)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "UserApplicatedLog not found"}

def get_user_applicated_logs_by_app_id(db: Session, application_id_input: int, page: int = 1, item_counts: int = 20) -> dict:
    """application_id 로 UserApplicatedLog 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(UserApplicatedLog).filter(UserApplicatedLog.application_id == application_id_input).count()
    logs = db.query(UserApplicatedLog).filter(UserApplicatedLog.application_id == application_id_input).offset(offset).limit(item_counts).all()
    return {
        "success": True,
        "user_applicated_logs": [log.to_dict() for log in logs],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }