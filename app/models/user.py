# models/user.py
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

Base = declarative_base()

class User(Base):
    """
    User 테이블 모델

    Attributes:
        user_id (str): 사용자 ID (PK)
        user_email (str): 사용자 이메일 (NN, unique)
        user_level (int): 사용자 레벨 (FK)
        user_password (str): 사용자 비밀번호 (NN) - 암호화되어 저장되어야 함
        created_date (datetime): 생성일시 (NN)
        last_updated_date (datetime): 최종 수정일시 (NN)
        user_bookmark (JSON): 북마크 정보 (JSON)
        user_applicated (JSON): 지원 정보 (JSON)
    """
    __tablename__ = 'User'

    user_id = Column(String(255), primary_key=True, comment="사용자 ID")
    user_email = Column(String(255), nullable=False, unique=True, comment="사용자 이메일")
    user_level = Column(Integer, comment="사용자 레벨 (FK)")  # ForeignKey는 관계 설정 시 추가
    user_password = Column(String(255), nullable=False, comment="사용자 비밀번호 (암호화)")
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow, comment="생성일시")
    last_updated_date = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="최종 수정일시")
    user_bookmark = Column(JSON, comment="북마크 정보")
    user_applicated = Column(JSON, comment="지원 정보")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_email": self.user_email,
            "user_level": self.user_level,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "last_updated_date": self.last_updated_date.isoformat() if self.last_updated_date else None,
            "user_bookmark": self.user_bookmark,
            "user_applicated": self.user_applicated,
        }

def create_user(db: Session, user_id: str, user_email: str, user_level: int, user_password: str, user_bookmark=None, user_applicated=None):
    """새로운 User 레코드 생성"""
    try:
        db_user = User(user_id=user_id, user_email=user_email, user_level=user_level, user_password=user_password, user_bookmark=user_bookmark, user_applicated = user_applicated)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user.to_dict(), "사용자가 성공적으로 생성되었습니다."
    except IntegrityError:
        db.rollback()
        return None, "이미 존재하는 사용자 ID 또는 이메일입니다." #unique 제약 조건 위반
    except Exception as e:
        db.rollback()
        return None, f"사용자 생성 중 오류가 발생했습니다: {str(e)}"

def get_user(db: Session, user_id: str):
    """user_id로 User 레코드 조회"""
    try:
        user_obj = db.query(User).filter(User.user_id == user_id).first()
        if user_obj:
            return user_obj.to_dict(), "사용자 조회 성공"
        return None, "해당하는 사용자가 없습니다."
    except Exception as e:
        return None, f"사용자 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_by_email(db: Session, user_email: str):
    """user_email로 User 레코드 조회"""
    try:
        user_obj = db.query(User).filter(User.user_email == user_email).first()
        if user_obj:
            return user_obj.to_dict(), "사용자 조회 성공"
        return None, "해당하는 이메일의 사용자가 없습니다."
    except Exception as e:
        return None, f"사용자 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """User 레코드 목록 조회 (페이지네이션 지원)"""
    try:
        query = db.query(User)
        if pagination:
            users = query.offset((page - 1) * per_page).limit(per_page).all()
        else:
            users = query.all()
        user_list = [user.to_dict() for user in users]
        return user_list, "사용자 목록 조회 성공"
    except Exception as e:
        return None, f"사용자 목록 조회 중 오류가 발생했습니다: {str(e)}"

def update_user(db: Session, user_id: str, user_email: str = None, user_level: int = None, new_password: str = None, user_bookmark = None, user_applicated = None):
    """User 레코드 업데이트"""
    try:
        user_obj = db.query(User).filter(User.user_id == user_id).first()
        if user_obj:
            if user_email:
                user_obj.user_email = user_email
            if user_level:
                user_obj.user_level = user_level
            if new_password:
                user_obj.user_password = new_password
            if user_bookmark is not None: # None이 들어올 경우를 대비
                user_obj.user_bookmark = user_bookmark
            if user_applicated is not None:
                user_obj.user_applicated = user_applicated

            db.commit()
            db.refresh(user_obj)
            return user_obj.to_dict(), "사용자 정보가 성공적으로 수정되었습니다."
        return None, "해당하는 사용자가 없습니다."
    except IntegrityError as e: #user_email unique 조건에 위배되는 경우 발생
        db.rollback()
        if "Duplicate entry" in str(e):
            return None, "이미 사용중인 이메일입니다."
        return None, f"사용자 정보 수정 중 무결성 오류가 발생했습니다: {str(e)}"
    except Exception as e:
        db.rollback()
        return None, f"사용자 정보 수정 중 오류가 발생했습니다: {str(e)}"

def delete_user(db: Session, user_id: str):
    """User 레코드 삭제"""
    try:
        user_obj = db.query(User).filter(User.user_id == user_id).first()
        if user_obj:
            db.delete(user_obj)
            db.commit()
            return None, "사용자가 성공적으로 삭제되었습니다."
        return None, "해당하는 사용자가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"사용자 삭제 중 오류가 발생했습니다: {str(e)}"