# models/user_applicated.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.dialects.mysql import ENUM
import enum

from . import Base

class ApplicationStatus(enum.Enum):
    APPLIED = 0     # 지원
    CANCELLED = 1   # 취소
    ACCEPTED = 2    # 접수됨
    REJECTED = 3    # 거절됨


class UserApplicated(Base):
    """UserApplicated 테이블에 대한 SQLAlchemy 모델 클래스"""
    __tablename__ = "UserApplicated"

    application_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String(255), ForeignKey("User.user_id"), nullable=False)
    poster_id = Column(String(255), ForeignKey("JobPosting.poster_id"), nullable=False)
    application = Column(Text)
    application_status = Column(ENUM(ApplicationStatus), nullable=False) # enum 타입으로 변경

    # user = relationship("User", back_populates="applications")
    # job_posting = relationship("JobPosting", back_populates="user_applications")

    def to_dict(self):
        """UserApplicated 객체를 딕셔너리로 변환합니다."""
        return {
            "application_id": self.application_id,
            "user_id": self.user_id,
            "poster_id": self.poster_id,
            "application": self.application,
            "application_status": self.application_status.value if self.application_status else None, # enum 값인 value를 가져오도록 수정. None 처리 추가
        }

def get_user_applicateds(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """UserApplicated 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(UserApplicated).count()
    applicateds = db.query(UserApplicated).offset(offset).limit(item_counts).all()
    return {
        "success": True,
        "user_applicateds": [applicated.to_dict() for applicated in applicateds],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_user_applicated(db: Session, user_id: str, poster_id: str, application: str, application_status: ApplicationStatus) -> dict:
    """새로운 UserApplicated를 생성하는 함수"""
    try:
        new_applicated = UserApplicated(user_id=user_id, poster_id=poster_id, application=application, application_status=application_status)
        db.add(new_applicated)
        db.commit()
        db.refresh(new_applicated)
        return {"success": True, "user_applicated": new_applicated.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    
def get_user_applicated_by_id(db: Session, application_id_input: int) -> dict:
    """application_id로 UserApplicated 정보를 가져오는 함수"""
    applicated = db.query(UserApplicated).filter(UserApplicated.application_id == application_id_input).first()
    if applicated:
        return {"success": True, "user_applicated": applicated.to_dict()}
    else:
        return {"success": False, "message": "UserApplicated not found"}

def update_user_applicated(db: Session, application_id_input: int, new_application: str = None, new_application_status: ApplicationStatus = None) -> dict:
    """기존 UserApplicated 정보를 수정하는 함수"""
    applicated = db.query(UserApplicated).filter(UserApplicated.application_id == application_id_input).first()
    if applicated:
        try:
            if new_application is not None:
                applicated.application = new_application
            if new_application_status is not None:
                applicated.application_status = new_application_status
            db.commit()
            return {"success": True, "user_applicated": applicated.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "UserApplicated not found"}

def delete_user_applicated(db: Session, application_id_input: int) -> dict:
    """기존 UserApplicated 정보를 삭제하는 함수"""
    applicated = db.query(UserApplicated).filter(UserApplicated.application_id == application_id_input).first()
    if applicated:
        try:
            db.delete(applicated)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "UserApplicated not found"}