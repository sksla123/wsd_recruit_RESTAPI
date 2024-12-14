# models/sal_code.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class SalCode(Base):
    """
    SalCode 테이블 모델

    Attributes:
        sal_code (int): 급여 코드 (PK)
        sal_name (str): 급여 명칭
    """
    __tablename__ = 'SalCode'

    sal_code = Column(Integer, primary_key=True)
    sal_name = Column(String(255), nullable=False)

    def to_dict(self):
        """모델 객체를 딕셔너리로 변환"""
        return {
            "sal_code": self.sal_code,
            "sal_name": self.sal_name
        }

def create_sal_code(db: Session, sal_code: int, sal_name: str):
    """새로운 SalCode 레코드 생성"""
    try:
        db_sal_code = SalCode(sal_code=sal_code, sal_name=sal_name)
        db.add(db_sal_code)
        db.commit()
        db.refresh(db_sal_code)
        return db_sal_code.to_dict(), "급여 코드가 성공적으로 생성되었습니다."
    except IntegrityError:
        db.rollback()
        return None, "이미 존재하는 급여 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"급여 코드 생성 중 오류가 발생했습니다: {str(e)}"

def get_sal_code(db: Session, sal_code: int):
    """sal_code로 SalCode 레코드 조회"""
    try:
      sal_code_obj = db.query(SalCode).filter(SalCode.sal_code == sal_code).first()
      if sal_code_obj:
        return sal_code_obj.to_dict(), "급여 코드 조회 성공"
      return None, "해당하는 급여 코드가 없습니다."
    except Exception as e:
        return None, f"급여 코드 조회 중 오류가 발생했습니다: {str(e)}"

def get_sal_code_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """SalCode 레코드 목록 조회 (페이지네이션 지원)"""
    try:
      query = db.query(SalCode)
      if pagination:
          sal_codes = query.offset((page - 1) * per_page).limit(per_page).all()
      else:
          sal_codes = query.all()
      sal_code_list = [sal_code.to_dict() for sal_code in sal_codes]
      return sal_code_list, "급여 코드 목록 조회 성공"
    except Exception as e:
        return None, f"급여 코드 목록 조회 중 오류가 발생했습니다: {str(e)}"


def update_sal_code(db: Session, sal_code: int, new_sal_name: str):
    """SalCode 레코드 업데이트"""
    try:
      sal_code_obj = db.query(SalCode).filter(SalCode.sal_code == sal_code).first()
      if sal_code_obj:
        sal_code_obj.sal_name = new_sal_name
        db.commit()
        db.refresh(sal_code_obj)
        return sal_code_obj.to_dict(), "급여 코드가 성공적으로 수정되었습니다."
      return None, "해당하는 급여 코드가 없습니다."
    except IntegrityError:
      db.rollback()
      return None, "이미 존재하는 급여 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"급여 코드 수정 중 오류가 발생했습니다: {str(e)}"

def delete_sal_code(db: Session, sal_code: int):
    """SalCode 레코드 삭제"""
    try:
      sal_code_obj = db.query(SalCode).filter(SalCode.sal_code == sal_code).first()
      if sal_code_obj:
        db.delete(sal_code_obj)
        db.commit()
        return None, "급여 코드가 성공적으로 삭제되었습니다."
      return None, "해당하는 급여 코드가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"급여 코드 삭제 중 오류가 발생했습니다: {str(e)}"