# models/edu_code.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class EduCode(Base):
    """
    EduCode 테이블 모델

    Attributes:
        edu_code (int): 학력 코드 (PK)
        edu_name (str): 학력 명칭
    """
    __tablename__ = 'EduCode'

    edu_code = Column(Integer, primary_key=True)
    edu_name = Column(String(255), nullable=False)

    def to_dict(self):
        """모델 객체를 딕셔너리로 변환"""
        return {
            "edu_code": self.edu_code,
            "edu_name": self.edu_name
        }

def create_edu_code(db: Session, edu_code: int, edu_name: str):
    """새로운 EduCode 레코드 생성"""
    try:
        db_edu_code = EduCode(edu_code=edu_code, edu_name=edu_name)
        db.add(db_edu_code)
        db.commit()
        db.refresh(db_edu_code)
        return db_edu_code.to_dict(), "학력 코드가 성공적으로 생성되었습니다."
    except IntegrityError:
        db.rollback()
        return None, "이미 존재하는 학력 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"학력 코드 생성 중 오류가 발생했습니다: {str(e)}"

def get_edu_code(db: Session, edu_code: int):
    """edu_code로 EduCode 레코드 조회"""
    try:
      edu_code_obj = db.query(EduCode).filter(EduCode.edu_code == edu_code).first()
      if edu_code_obj:
        return edu_code_obj.to_dict(), "학력 코드 조회 성공"
      return None, "해당하는 학력 코드가 없습니다."
    except Exception as e:
        return None, f"학력 코드 조회 중 오류가 발생했습니다: {str(e)}"

def get_edu_code_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """EduCode 레코드 목록 조회 (페이지네이션 지원)"""
    try:
      query = db.query(EduCode)
      if pagination:
          edu_codes = query.offset((page - 1) * per_page).limit(per_page).all()
      else:
          edu_codes = query.all()
      edu_code_list = [edu_code.to_dict() for edu_code in edu_codes]
      return edu_code_list, "학력 코드 목록 조회 성공"
    except Exception as e:
        return None, f"학력 코드 목록 조회 중 오류가 발생했습니다: {str(e)}"

def update_edu_code(db: Session, edu_code: int, new_edu_name: str):
    """EduCode 레코드 업데이트"""
    try:
      edu_code_obj = db.query(EduCode).filter(EduCode.edu_code == edu_code).first()
      if edu_code_obj:
        edu_code_obj.edu_name = new_edu_name
        db.commit()
        db.refresh(edu_code_obj)
        return edu_code_obj.to_dict(), "학력 코드가 성공적으로 수정되었습니다."
      return None, "해당하는 학력 코드가 없습니다."