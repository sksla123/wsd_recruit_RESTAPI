# models/login_log.py
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

Base = declarative_base()

class LoginLog(Base):
    """
    LoginLog 테이블 모델

    Attributes:
        login_log_id (int): 로그인 로그 ID (PK, Auto Increment)
        login_date (datetime): 로그인 날짜 및 시간
        login_id (str): 로그인 ID (FK, User 테이블 참조)
        login_ip (str): 로그인 IP 주소
        login_device_info (str): 로그인 기기 정보
        login_success (bool): 로그인 성공 여부
    """
    __tablename__ = 'LoginLog'

    login_log_id = Column(Integer, primary_key=True, autoincrement=True, comment="로그인 로그 ID")
    login_date = Column(DateTime, default=datetime.utcnow, comment="로그인 날짜 및 시간")
    login_id = Column(String(255), ForeignKey('User.user_id'), comment="로그인 ID (User 테이블 참조)") # nullable=False 삭제. user 삭제 시 로그는 남아야함.
    login_ip = Column(String(255), comment="로그인 IP 주소")
    login_device_info = Column(Text, comment="로그인 기기 정보")
    login_success = Column(Boolean, comment="로그인 성공 여부") # INT 대신 Boolean 사용

    def to_dict(self):
        return {
            "login_log_id": self.login_log_id,
            "login_date": self.login_date.isoformat() if self.login_date else None,
            "login_id": self.login_id,
            "login_ip": self.login_ip,
            "login_device_info": self.login_device_info,
            "login_success": self.login_success
        }

def create_login_log(db: Session, login_id: str = None, login_ip: str = None, login_device_info: str = None, login_success: bool = False):
    """새로운 LoginLog 레코드 생성"""
    try:
        db_login_log = LoginLog(
            login_id=login_id,
            login_ip=login_ip,
            login_device_info=login_device_info,
            login_success=login_success
        )
        db.add(db_login_log)
        db.commit()
        db.refresh(db_login_log)
        return db_login_log.to_dict(), "로그인 로그가 생성되었습니다."
    except IntegrityError as e:
        db.rollback()
        return None, f"데이터베이스 무결성 오류: {str(e)}" #login_id FK 오류 발생 가능성 있음.
    except Exception as e:
        db.rollback()
        return None, f"로그인 로그 생성 중 오류가 발생했습니다: {str(e)}"

def get_login_log(db: Session, login_log_id: int):
    """login_log_id로 LoginLog 레코드 조회"""
    try:
        login_log_obj = db.query(LoginLog).filter(LoginLog.login_log_id == login_log_id).first()
        if login_log_obj:
            return login_log_obj.to_dict(), "로그인 로그 조회 성공"
        return None, "해당 login_log_id의 로그인 로그가 없습니다."
    except Exception as e:
        return None, f"로그인 로그 조회 중 오류가 발생했습니다: {str(e)}"

def get_login_log_list_by_login_id(db: Session, login_id: str):
  """login_id로 LoginLog 레코드 목록 조회"""
  try:
      login_log_list = db.query(LoginLog).filter(LoginLog.login_id == login_id).all()
      if login_log_list:
        result = [login_log.to_dict() for login_log in login_log_list]
        return result, f"해당 login_id({login_id})의 로그인 로그 목록 조회 성공"
      return None, f"해당 login_id({login_id})의 로그인 로그가 없습니다."
  except Exception as e:
      return None, f"로그인 로그 목록 조회 중 오류가 발생했습니다: {str(e)}"

def get_all_login_log_list(db: Session):
  """모든 LoginLog 레코드 목록 조회"""
  try:
      login_log_list = db.query(LoginLog).all()
      if login_log_list:
        result = [login_log.to_dict() for login_log in login_log_list]
        return result, f"모든 로그인 로그 목록 조회 성공"
      return None, f"로그인 로그가 없습니다."
  except Exception as e:
      return None, f"로그인 로그 목록 조회 중 오류가 발생했습니다: {str(e)}"