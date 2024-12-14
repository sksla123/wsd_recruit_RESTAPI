# models/edu_code.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class EduCode(Base):
    """
    EduCode 테이블 모델

    Attributes:
        edu_code (int): 학력 코드 (PK)
        edu_name (str): 학력 명칭 (NN)
    """
    __tablename__ = 'EduCode'

    edu_code = Column(Integer, primary_key=True, comment="학력 코드")
    edu_name = Column(String(255), nullable=False, comment="학력 명칭")

    def to_dict(self):
        """
        모델 객체를 딕셔너리로 변환

        Returns:
            dict: 모델의 데이터를 담은 딕셔너리
        """
        return {
            "edu_code": self.edu_code,
            "edu_name": self.edu_name
        }

def create_edu_code(db: Session, edu_code: int, edu_name: str):
    """
    새로운 EduCode 레코드 생성

    Args:
        db (Session): 데이터베이스 세션
        edu_code (int): 학력 코드
        edu_name (str): 학력 명칭

    Returns:
        tuple: (dict, str) - (생성된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        db_edu_code = EduCode(edu_code=edu_code, edu_name=edu_name)
        db.add(db_edu_code)
        db.commit()
        db.refresh(db_edu_code)  # DB에서 최신 데이터를 가져옴
        return db_edu_code.to_dict(), "학력 코드가 성공적으로 생성되었습니다."
    except IntegrityError:
        db.rollback()  # 오류 발생 시 롤백
        return None, "이미 존재하는 학력 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"학력 코드 생성 중 오류가 발생했습니다: {str(e)}"

def get_edu_code(db: Session, edu_code: int):
    """
    edu_code로 EduCode 레코드 조회

    Args:
        db (Session): 데이터베이스 세션
        edu_code (int): 조회할 학력 코드

    Returns:
        tuple: (dict, str) - (조회된 데이터, 메시지) 또는 (None, 메시지)
    """
    try:
        edu_code_obj = db.query(EduCode).filter(EduCode.edu_code == edu_code).first()
        if edu_code_obj:
            return edu_code_obj.to_dict(), "학력 코드 조회 성공"
        return None, "해당하는 학력 코드가 없습니다."
    except Exception as e:
        return None, f"학력 코드 조회 중 오류가 발생했습니다: {str(e)}"

def get_edu_code_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """
    EduCode 레코드 목록 조회 (페이지네이션 지원)

    Args:
        db (Session): 데이터베이스 세션
        page (int): 페이지 번호 (기본값: 1)
        per_page (int): 페이지당 항목 수 (기본값: 20)
        pagination (bool): 페이지네이션 사용 여부 (기본값: False)

    Returns:
        tuple: (list, str) - (조회된 데이터 목록, 메시지) 또는 (None, 메시지)
    """
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
    """
    EduCode 레코드 업데이트

    Args:
        db (Session): 데이터베이스 세션
        edu_code (int): 수정할 학력 코드
        new_edu_name (str): 새로운 학력 명칭

    Returns:
        tuple: (dict, str) - (업데이트된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        edu_code_obj = db.query(EduCode).filter(EduCode.edu_code == edu_code).first()
        if edu_code_obj:
            edu_code_obj.edu_name = new_edu_name
            db.commit()
            db.refresh(edu_code_obj)
            return edu_code_obj.to_dict(), "학력 코드가 성공적으로 수정되었습니다."
        return None, "해당하는 학력 코드가 없습니다."
    except IntegrityError:
        db.rollback()
        return None, "이미 존재하는 학력 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"학력 코드 수정 중 오류가 발생했습니다: {str(e)}"

def delete_edu_code(db: Session, edu_code: int):
    """
    EduCode 레코드 삭제

    Args:
        db (Session): 데이터베이스 세션
        edu_code (int): 삭제할 학력 코드

    Returns:
        tuple: (None, str) - (None, 메시지)
    """
    try:
        edu_code_obj = db.query(EduCode).filter(EduCode.edu_code == edu_code).first()
        if edu_code_obj:
            db.delete(edu_code_obj)
            db.commit()
            return None, "학력 코드가 성공적으로 삭제되었습니다."
        return None, "해당하는 학력 코드가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"학력 코드 삭제 중 오류가 발생했습니다: {str(e)}"