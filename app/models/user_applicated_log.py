# models/user_applicated_log.py
import enum
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Enum
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

Base = declarative_base()

class ApplicationStatus(enum.Enum):
    APPLIED = 0  # 지원
    CANCELLED = 1  # 취소
    ACCEPTED = 2 # 접수됨

class UserApplicatedLog(Base):
    """
    UserApplicatedLog 테이블 모델

    Attributes:
        application_log_id (int): 지원 로그 ID (PK, Auto Increment)
        application_id (int): 지원 ID (FK, UserApplicated 테이블 참조)
        applicated_at (datetime): 지원/취소 시간
        user_id (str): 사용자 ID (FK, User 테이블 참조)
        poster_id (str): 공고 ID (FK, JobPosting 테이블 참조)
        status (ApplicationStatus): 지원 상태 (Enum)
    """
    __tablename__ = 'UserApplicatedLog'

    application_log_id = Column(Integer, primary_key=True, autoincrement=True, comment="지원 로그 ID")
    application_id = Column(Integer, ForeignKey('UserApplicated.application_id'), nullable=False, comment="지원 ID")
    applicated_at = Column(DateTime, default=datetime.utcnow, comment="지원/취소 시간")
    user_id = Column(String(255), ForeignKey('User.user_id'), nullable=False, comment="사용자 ID")
    poster_id = Column(String(255), ForeignKey('JobPosting.poster_id'), nullable=False, comment="공고 ID")
    status = Column(Enum(ApplicationStatus), nullable=False, comment="지원 상태")

    def to_dict(self):
        return {
            "application_log_id": self.application_log_id,
            "application_id": self.application_id,
            "applicated_at": self.applicated_at.isoformat() if self.applicated_at else None,
            "user_id": self.user_id,
            "poster_id": self.poster_id,
            "status": self.status.value # Enum value를 int로 반환
        }

def create_user_applicated_log(db: Session, application_id: int, user_id: str, poster_id: str, status: ApplicationStatus):
    """새로운 UserApplicatedLog 레코드 생성"""
    try:
        db_user_applicated_log = UserApplicatedLog(
            application_id=application_id,
            user_id=user_id,
            poster_id=poster_id,
            status=status
        )
        db.add(db_user_applicated_log)
        db.commit()
        db.refresh(db_user_applicated_log)
        return db_user_applicated_log.to_dict(), "지원 로그가 기록되었습니다."
    except IntegrityError as e:
        db.rollback()
        return None, f"데이터베이스 무결성 오류 (FK 제약 조건 위반): {str(e)}"
    except Exception as e:
        db.rollback()
        return None, f"지원 로그 기록 중 오류가 발생했습니다: {str(e)}"

def get_user_applicated_log(db: Session, application_log_id: int):
    """application_log_id로 UserApplicatedLog 레코드 조회"""
    try:
        user_applicated_log_obj = db.query(UserApplicatedLog).filter(UserApplicatedLog.application_log_id == application_log_id).first()
        if user_applicated_log_obj:
            return user_applicated_log_obj.to_dict(), "지원 로그 조회 성공"
        return None, "해당 지원 로그가 없습니다."
    except Exception as e:
        return None, f"지원 로그 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_applicated_log_list_by_application_id(db: Session, application_id: int):
    """application_id로 UserApplicatedLog 레코드 목록 조회"""
    try:
        user_applicated_log_list = db.query(UserApplicatedLog).filter(UserApplicatedLog.application_id == application_id).all()
        if user_applicated_log_list:
            result = [log.to_dict() for log in user_applicated_log_list]
            return result, f"해당 application_id({application_id})의 지원 로그 목록 조회 성공"
        return None, f"해당 application_id({application_id})의 지원 로그가 없습니다."
    except Exception as e:
        return None, f"지원 로그 목록 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_applicated_log_list_by_user_id(db: Session, user_id: str):
    """user_id로 UserApplicatedLog 레코드 목록 조회"""
    try:
        user_applicated_log_list = db.query(UserApplicatedLog).filter(UserApplicatedLog.user_id == user_id).all()
        if user_applicated_log_list:
            result = [log.to_dict() for log in user_applicated_log_list]
            return result, f"해당 user_id({user_id})의 지원 로그 목록 조회 성공"
        return None, f"해당 user_id({user_id})의 지원 로그가 없습니다."
    except Exception as e:
        return None, f"지원 로그 목록 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_applicated_log_list_by_poster_id(db: Session, poster_id: str):
    """poster_id로 UserApplicatedLog 레코드 목록 조회"""
    try:
        user_applicated_log_list = db.query(UserApplicatedLog).filter(UserApplicatedLog.poster_id == poster_id).all()
        if user_applicated_log_list:
            result = [log.to_dict() for log in user_applicated_log_list]
            return result, f"해당 poster_id({poster_id})의 지원 로그 목록 조회 성공"
        return None, f"해당 poster_id({poster_id})의 지원 로그가 없습니다."
    except Exception as e:
        return None, f"지원 로그 목록 조회 중 오류가 발생했습니다: {str(e)}"

# 삭제 기능은 이력 테이블이므로 일반적으로 필요하지 않으므로 생략