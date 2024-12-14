# models/job_code.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

class JobCode(Base):
    """
    JobCode 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "JobCode"

    job_code = Column(Integer, primary_key=True)
    job_name = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "job_code": self.job_code,
            "job_name": self.job_name
        }

def get_job_codes(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """
    JobCode 목록을 조회하는 함수 (Pagination 적용)
    """
    offset = (page - 1) * item_counts
    job_codes = db.query(JobCode).offset(offset).limit(item_counts).all()
    total_count = db.query(JobCode).count()
    return {
        "job_codes": [job_code.to_dict() for job_code in job_codes],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_job_code(db: Session, job_code: int, job_name: str) -> dict:
    """
    새로운 JobCode를 생성하는 함수
    """
    try:
        new_job_code = JobCode(job_code=job_code, job_name=job_name)
        db.add(new_job_code)
        db.commit()
        db.refresh(new_job_code)
        return {"success": True, "job_code": new_job_code.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_job_code_by_id(db: Session, job_code_id: int) -> dict: #인자 이름 통일
    """
    job_code로 JobCode 정보를 가져오는 함수
    """
    job_code = db.query(JobCode).filter(JobCode.job_code == job_code_id).first() #필터 조건 수정
    if job_code:
        return {"success": True, "job_code": job_code.to_dict()}
    else:
        return {"success": False, "message": "JobCode not found"}

def update_job_code(db: Session, job_code_id: int, new_job_name: str) -> dict: #인자 이름 통일
    """
    기존 JobCode 정보를 수정하는 함수
    """
    job_code = db.query(JobCode).filter(JobCode.job_code == job_code_id).first() #필터 조건 수정
    if job_code:
        try:
            job_code.job_name = new_job_name
            db.commit()
            return {"success": True, "job_code": job_code.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "JobCode not found"}

def delete_job_code(db: Session, job_code_id: int) -> dict: #인자 이름 통일
    """
    기존 JobCode 정보를 삭제하는 함수
    """
    job_code = db.query(JobCode).filter(JobCode.job_code == job_code_id).first() #필터 조건 수정
    if job_code:
        try:
            db.delete(job_code)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "JobCode not found"}