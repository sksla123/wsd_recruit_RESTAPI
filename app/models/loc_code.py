# models/loc_code.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class LocCode(Base):
    """
    LocCode 테이블 모델

    Attributes:
        loc_code (int): 지역 코드 (PK)
        loc_name (str): 지역 명칭 (NN)
    """
    __tablename__ = 'LocCode'

    loc_code = Column(Integer, primary_key=True, comment="지역 코드")
    loc_name = Column(String(255), nullable=False, comment="지역 명칭")

    def to_dict(self):
        """
        모델 객체를 딕셔너리로 변환

        Returns:
            dict: 모델의 데이터를 담은 딕셔너리
        """
        return {
            "loc_code": self.loc_code,
            "loc_name": self.loc_name
        }

def create_loc_code(db: Session, loc_code: int, loc_name: str):
    """
    새로운 LocCode 레코드 생성

    Args:
        db (Session): 데이터베이스 세션
        loc_code (int): 지역 코드
        loc_name (str): 지역 명칭

    Returns:
        tuple: (dict, str) - (생성된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        db_loc_code = LocCode(loc_code=loc_code, loc_name=loc_name)
        db.add(db_loc_code)
        db.commit()
        db.refresh(db_loc_code)
        return db_loc_code.to_dict(), "지역 코드가 성공적으로 생성되었습니다."
    except IntegrityError:
        db.rollback()
        return None, "이미 존재하는 지역 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"지역 코드 생성 중 오류가 발생했습니다: {str(e)}"

def get_loc_code(db: Session, loc_code: int):
    """
    loc_code로 LocCode 레코드 조회

    Args:
        db (Session): 데이터베이스 세션
        loc_code (int): 조회할 지역 코드

    Returns:
        tuple: (dict, str) - (조회된 데이터, 메시지) 또는 (None, 메시지)
    """
    try:
        loc_code_obj = db.query(LocCode).filter(LocCode.loc_code == loc_code).first()
        if loc_code_obj:
            return loc_code_obj.to_dict(), "지역 코드 조회 성공"
        return None, "해당하는 지역 코드가 없습니다."
    except Exception as e:
        return None, f"지역 코드 조회 중 오류가 발생했습니다: {str(e)}"

def get_loc_code_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """
    LocCode 레코드 목록 조회 (페이지네이션 지원)

    Args:
        db (Session): 데이터베이스 세션
        page (int): 페이지 번호 (기본값: 1)
        per_page (int): 페이지당 항목 수 (기본값: 20)
        pagination (bool): 페이지네이션 사용 여부 (기본값: False)

    Returns:
        tuple: (list, str) - (조회된 데이터 목록, 메시지) 또는 (None, 메시지)
    """
    try:
        query = db.query(LocCode)
        if pagination:
            loc_codes = query.offset((page - 1) * per_page).limit(per_page).all()
        else:
            loc_codes = query.all()
        loc_code_list = [loc_code.to_dict() for loc_code in loc_codes]
        return loc_code_list, "지역 코드 목록 조회 성공"
    except Exception as e:
        return None, f"지역 코드 목록 조회 중 오류가 발생했습니다: {str(e)}"

def update_loc_code(db: Session, loc_code: int, new_loc_name: str):
    """
    LocCode 레코드 업데이트

    Args:
        db (Session): 데이터베이스 세션
        loc_code (int): 수정할 지역 코드
        new_loc_name (str): 새로운 지역 명칭

    Returns:
        tuple: (dict, str) - (업데이트된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        loc_code_obj = db.query(LocCode).filter(LocCode.loc_code == loc_code).first()
        if loc_code_obj:
            loc_code_obj.loc_name = new_loc_name
            db.commit()
            db.refresh(loc_code_obj)
            return loc_code_obj.to_dict(), "지역 코드가 성공적으로 수정되었습니다."
        return None, "해당하는 지역 코드가 없습니다."
    except IntegrityError:
      db.rollback()
      return None, "이미 존재하는 지역 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"지역 코드 수정 중 오류가 발생했습니다: {str(e)}"

def delete_loc_code(db: Session, loc_code: int):
    """
    LocCode 레코드 삭제

    Args:
        db (Session): 데이터베이스 세션
        loc_code (int): 삭제할 지역 코드

    Returns:
        tuple: (None, str) - (None, 메시지)
    """
    try:
        loc_code_obj = db.query(LocCode).filter(LocCode.loc_code == loc_code).first()
        if loc_code_obj:
            db.delete(loc_code_obj)
            db.commit()
            return None, "지역 코드가 성공적으로 삭제되었습니다."
        return None, "해당하는 지역 코드가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"지역 코드 삭제 중 오류가 발생했습니다: {str(e)}"