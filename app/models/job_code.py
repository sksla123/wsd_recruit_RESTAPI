# models/job_code.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class JobCode(Base):
    """
    JobCode 테이블 모델

    Attributes:
        job_code (int): 직무 코드 (PK)
        job_name (str): 직무 명칭 (NN)
    """
    __tablename__ = 'JobCode'

    job_code = Column(Integer, primary_key=True, comment="직무 코드")
    job_name = Column(String(255), nullable=False, comment="직무 명칭")

    def to_dict(self):
        """
        모델 객체를 딕셔너리로 변환

        Returns:
            dict: 모델의 데이터를 담은 딕셔너리
        """
        return {
            "job_code": self.job_code,
            "job_name": self.job_name
        }

def create_job_code(db: Session, job_code: int, job_name: str):
    """
    새로운 JobCode 레코드 생성

    Args:
        db (Session): 데이터베이스 세션
        job_code (int): 직무 코드
        job_name (str): 직무 명칭

    Returns:
        tuple: (dict, str) - (생성된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        db_job_code = JobCode(job_code=job_code, job_name=job_name)
        db.add(db_job_code)
        db.commit()
        db.refresh(db_job_code)
        return db_job_code.to_dict(), "직무 코드가 성공적으로 생성되었습니다."
    except IntegrityError:
        db.rollback()
        return None, "이미 존재하는 직무 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"직무 코드 생성 중 오류가 발생했습니다: {str(e)}"

def get_job_code(db: Session, job_code: int):
    """
    job_code로 JobCode 레코드 조회

    Args:
        db (Session): 데이터베이스 세션
        job_code (int): 조회할 직무 코드

    Returns:
        tuple: (dict, str) - (조회된 데이터, 메시지) 또는 (None, 메시지)
    """
    try:
        job_code_obj = db.query(JobCode).filter(JobCode.job_code == job_code).first()
        if job_code_obj:
            return job_code_obj.to_dict(), "직무 코드 조회 성공"
        return None, "해당하는 직무 코드가 없습니다."
    except Exception as e:
        return None, f"직무 코드 조회 중 오류가 발생했습니다: {str(e)}"

def get_job_code_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """
    JobCode 레코드 목록 조회 (페이지네이션 지원)

    Args:
        db (Session): 데이터베이스 세션
        page (int): 페이지 번호 (기본값: 1)
        per_page (int): 페이지당 항목 수 (기본값: 20)
        pagination (bool): 페이지네이션 사용 여부 (기본값: False)

    Returns:
        tuple: (list, str) - (조회된 데이터 목록, 메시지) 또는 (None, 메시지)
    """
    try:
        query = db.query(JobCode)
        if pagination:
            job_codes = query.offset((page - 1) * per_page).limit(per_page).all()
        else:
            job_codes = query.all()
        job_code_list = [job_code.to_dict() for job_code in job_codes]
        return job_code_list, "직무 코드 목록 조회 성공"
    except Exception as e:
        return None, f"직무 코드 목록 조회 중 오류가 발생했습니다: {str(e)}"

def update_job_code(db: Session, job_code: int, new_job_name: str):
    """
    JobCode 레코드 업데이트

    Args:
        db (Session): 데이터베이스 세션
        job_code (int): 수정할 직무 코드
        new_job_name (str): 새로운 직무 명칭

    Returns:
        tuple: (dict, str) - (업데이트된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        job_code_obj = db.query(JobCode).filter(JobCode.job_code == job_code).first()
        if job_code_obj:
            job_code_obj.job_name = new_job_name
            db.commit()
            db.refresh(job_code_obj)
            return job_code_obj.to_dict(), "직무 코드가 성공적으로 수정되었습니다."
        return None, "해당하는 직무 코드가 없습니다."
    except IntegrityError:
      db.rollback()
      return None, "이미 존재하는 직무 코드입니다."
    except Exception as e:
        db.rollback()
        return None, f"직무 코드 수정 중 오류가 발생했습니다: {str(e)}"

def delete_job_code(db: Session, job_code: int):
    """
    JobCode 레코드 삭제

    Args:
        db (Session): 데이터베이스 세션
        job_code (int): 삭제할 직무 코드

    Returns:
        tuple: (None, str) - (None, 메시지)
    """
    try:
        job_code_obj = db.query(JobCode).filter(JobCode.job_code == job_code).first()
        if job_code_obj:
            db.delete(job_code_obj)
            db.commit()
            return None, "직무 코드가 성공적으로 삭제되었습니다."
        return None, "해당하는 직무 코드가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"직무 코드 삭제 중 오류가 발생했습니다: {str(e)}"