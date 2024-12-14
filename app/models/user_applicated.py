# models/user_applicated.py
from sqlalchemy import Column, String, ForeignKey, Integer, Text
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class UserApplicated(Base):
    """
    UserApplicated 테이블 모델

    Attributes:
        application_id (int): 지원 ID (PK, Auto Increment)
        user_id (str): 사용자 ID (FK, User 테이블 참조)
        poster_id (str): 공고 ID (FK, JobPosting 테이블 참조)
        application (str): 지원 내용 (TEXT)
        application_status (int): 지원 상태 (정수형)
    """
    __tablename__ = 'UserApplicated'

    application_id = Column(Integer, primary_key=True, autoincrement=True, comment="지원 ID")
    user_id = Column(String(255), ForeignKey('User.user_id'), nullable=False, comment="사용자 ID")
    poster_id = Column(String(255), ForeignKey('JobPosting.poster_id'), nullable=False, comment="공고 ID")
    application = Column(Text, comment="지원 내용")
    application_status = Column(Integer, comment="지원 상태")

    def to_dict(self):
        return {
            "application_id": self.application_id,
            "user_id": self.user_id,
            "poster_id": self.poster_id,
            "application": self.application,
            "application_status": self.application_status
        }

def create_user_applicated(db: Session, user_id: str, poster_id: str, application: str = None, application_status: int = None):
    """새로운 UserApplicated 레코드 생성"""
    try:
        db_user_applicated = UserApplicated(user_id=user_id, poster_id=poster_id, application=application, application_status=application_status)
        db.add(db_user_applicated)
        db.commit()
        db.refresh(db_user_applicated)
        return db_user_applicated.to_dict(), "지원이 완료되었습니다."
    except IntegrityError as e:
        db.rollback()
        return None, f"데이터베이스 무결성 오류 (FK 제약 조건 위반): {str(e)}" # 중복 지원은 이제 DB단에서 막지 않음 (application_id가 PK 이므로)
    except Exception as e:
        db.rollback()
        return None, f"지원 처리 중 오류가 발생했습니다: {str(e)}"

def get_user_applicated(db: Session, application_id: int):
    """application_id로 UserApplicated 레코드 조회"""
    try:
        user_applicated_obj = db.query(UserApplicated).filter(UserApplicated.application_id == application_id).first()
        if user_applicated_obj:
            return user_applicated_obj.to_dict(), "지원 정보 조회 성공"
        return None, "해당 지원 내역이 없습니다."
    except Exception as e:
        return None, f"지원 정보 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_applicated_list_by_user_id(db: Session, user_id: str):
    """user_id로 UserApplicated 레코드 목록 조회 (사용자의 지원 목록)"""
    try:
        user_applicated_list = db.query(UserApplicated).filter(UserApplicated.user_id == user_id).all()
        if user_applicated_list:
            result = [user_applicated.to_dict() for user_applicated in user_applicated_list]
            return result, f"해당 user_id({user_id})의 지원 목록 조회 성공"
        return None, f"해당 user_id({user_id})의 지원 내역이 없습니다."
    except Exception as e:
        return None, f"지원 목록 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_applicated_list_by_poster_id(db: Session, poster_id: str):
    """poster_id로 UserApplicated 레코드 목록 조회 (공고에 지원한 사용자 목록)"""
    try:
        user_applicated_list = db.query(UserApplicated).filter(UserApplicated.poster_id == poster_id).all()
        if user_applicated_list:
            result = [user_applicated.to_dict() for user_applicated in user_applicated_list]
            return result, f"해당 poster_id({poster_id})에 지원한 사용자 목록 조회 성공"
        return None, f"해당 poster_id({poster_id})에 지원한 사용자가 없습니다."
    except Exception as e:
        return None, f"지원 목록 조회 중 오류가 발생했습니다: {str(e)}"

def update_user_applicated(db: Session, application_id: int, application: str = None, application_status: int = None):
    """UserApplicated 레코드 업데이트 (지원 내용 수정)"""
    try:
        user_applicated_obj = db.query(UserApplicated).filter(UserApplicated.application_id == application_id).first()
        if user_applicated_obj:
            if application is not None:
                user_applicated_obj.application = application
            if application_status is not None:
                user_applicated_obj.application_status = application_status
            db.commit()
            db.refresh(user_applicated_obj)
            return user_applicated_obj.to_dict(), "지원이 수정되었습니다."
        return None, "해당 지원 내역이 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"지원 수정 중 오류가 발생했습니다: {str(e)}"



def delete_user_applicated(db: Session, application_id: int):
    """UserApplicated 레코드 삭제 (지원 취소)"""
    try:
        user_applicated_obj = db.query(UserApplicated).filter(UserApplicated.application_id == application_id).first()
        if user_applicated_obj:
            db.delete(user_applicated_obj)
            db.commit()
            return None, "지원이 성공적으로 취소되었습니다."
        return None, "해당 지원 내역이 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"지원 취소 중 오류가 발생했습니다: {str(e)}"

# user_id 혹은 poster_id 만으로 삭제하는 함수는 일반적으로 필요하지 않으므로 생략합니다.