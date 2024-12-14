# models/login.py
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Text
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

Base = declarative_base()

class Login(Base):
    """
    Login 테이블 모델

    Attributes:
        refresh_id (int): Refresh ID (PK, Auto Increment)
        user_id (str): 사용자 ID (FK, User 테이블 참조)
        refresh_token (str): Refresh Token
        created_at (datetime): 생성 시간
        expires_at (datetime): 만료 시간
        login_device_info (str): 로그인 기기 정보
        login_ip (str): 로그인 IP 주소
    """
    __tablename__ = 'Login'

    refresh_id = Column(Integer, primary_key=True, autoincrement=True, comment="Refresh ID")
    user_id = Column(String(255), ForeignKey('User.user_id'), nullable=False, comment="사용자 ID")
    refresh_token = Column(Text, comment="Refresh Token")
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 시간")
    expires_at = Column(DateTime, comment="만료 시간")
    login_device_info = Column(Text, comment="로그인 기기 정보")
    login_ip = Column(String(255), comment="로그인 IP 주소")

    def to_dict(self):
        return {
            "refresh_id": self.refresh_id,
            "user_id": self.user_id,
            "refresh_token": self.refresh_token,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "login_device_info": self.login_device_info,
            "login_ip": self.login_ip
        }

def create_login(db: Session, user_id: str, refresh_token: str, expires_at: datetime, login_device_info: str = None, login_ip: str = None):
    """새로운 Login 레코드 생성"""
    try:
        db_login = Login(
            user_id=user_id,
            refresh_token=refresh_token,
            expires_at=expires_at,
            login_device_info=login_device_info,
            login_ip=login_ip
        )
        db.add(db_login)
        db.commit()
        db.refresh(db_login)
        return db_login.to_dict(), "로그인 정보가 생성되었습니다."
    except IntegrityError as e:
        db.rollback()
        return None, f"데이터베이스 무결성 오류 (FK 제약 조건 위반): {str(e)}"
    except Exception as e:
        db.rollback()
        return None, f"로그인 정보 생성 중 오류가 발생했습니다: {str(e)}"

def get_login(db: Session, refresh_id: int):
    """refresh_id로 Login 레코드 조회"""
    try:
        login_obj = db.query(Login).filter(Login.refresh_id == refresh_id).first()
        if login_obj:
            return login_obj.to_dict(), "로그인 정보 조회 성공"
        return None, "해당 refresh_id의 로그인 정보가 없습니다."
    except Exception as e:
        return None, f"로그인 정보 조회 중 오류가 발생했습니다: {str(e)}"

def get_login_by_user_id(db: Session, user_id: str):
    """user_id로 Login 레코드 조회"""
    try:
        login_obj = db.query(Login).filter(Login.user_id == user_id).order_by(Login.created_at.desc()).first()  #가장 최근의 로그인 정보를 가져옴.
        if login_obj:
            return login_obj.to_dict(), "로그인 정보 조회 성공"
        return None, "해당 user_id의 로그인 정보가 없습니다."
    except Exception as e:
        return None, f"로그인 정보 조회 중 오류가 발생했습니다: {str(e)}"
    
def delete_login(db: Session, refresh_id: int):
    """refresh_id로 Login 레코드 삭제"""
    try:
        login_obj = db.query(Login).filter(Login.refresh_id == refresh_id).first()
        if login_obj:
            db.delete(login_obj)
            db.commit()
            return None, "로그인 정보가 삭제되었습니다."
        return None, "해당 refresh_id의 로그인 정보가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"로그인 정보 삭제 중 오류가 발생했습니다: {str(e)}"

def delete_login_by_user_id(db: Session, user_id: str):
    """user_id로 모든 Login 레코드 삭제 (로그아웃 시 사용 가능)"""
    try:
      deleted_count = db.query(Login).filter(Login.user_id == user_id).delete()
      db.commit()
      if deleted_count > 0:
        return None, f"user_id({user_id})의 모든 로그인 정보 {deleted_count}개가 삭제되었습니다."
      else:
        return None, f"user_id({user_id})의 로그인 정보가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"로그인 정보 삭제 중 오류가 발생했습니다: {str(e)}"

def update_refresh_token(db: Session, refresh_id: int, new_refresh_token: str, new_expires_at: datetime):
    try:
        login_obj = db.query(Login).filter(Login.refresh_id == refresh_id).first()
        if login_obj:
            login_obj.refresh_token = new_refresh_token
            login_obj.expires_at = new_expires_at
            db.commit()
            db.refresh(login_obj)
            return login_obj.to_dict(), "리프레시 토큰이 갱신되었습니다."
        return None, "해당 refresh_id가 존재하지 않습니다."
    except Exception as e:
        db.rollback()
        return None, f"리프레시 토큰 갱신 중 오류가 발생했습니다: {str(e)}"