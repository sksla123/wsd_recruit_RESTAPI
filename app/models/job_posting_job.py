# models/job_posting_job.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import and_

from . import Base

class JobPostingJob(Base):
    """JobPostingJob 테이블에 대한 SQLAlchemy 모델 클래스"""
    __tablename__ = "JobPostingJob"

    poster_id = Column(String(255), ForeignKey("JobPosting.poster_id"), primary_key=True, nullable=False)
    job_code = Column(Integer, ForeignKey("JobCode.job_code"), primary_key=True, nullable=False)

    # job_posting = relationship("JobPosting", back_populates="job_posting_jobs")
    # job_code_info = relationship("JobCode", back_populates="job_posting_jobs")

    def to_dict(self):
        """JobPostingJob 객체를 딕셔너리로 변환합니다."""
        return {
            "poster_id": self.poster_id,
            "job_code": self.job_code
        }

def get_job_posting_jobs(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """JobPostingJob 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(JobPostingJob).count()
    postings = db.query(JobPostingJob).offset(offset).limit(item_counts).all()
    return {
        "success": True,
        "job_posting_jobs": [posting.to_dict() for posting in postings],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_job_posting_job(db: Session, poster_id: str, job_code: int) -> dict:
    """새로운 JobPostingJob을 생성하는 함수"""
    try:
        new_posting_job = JobPostingJob(poster_id=poster_id, job_code=job_code)
        db.add(new_posting_job)
        db.commit()
        db.refresh(new_posting_job)
        return {"success": True, "job_posting_job": new_posting_job.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_job_posting_job_by_ids(db: Session, poster_id_input: str, job_code_input: int) -> dict:
    """poster_id와 job_code로 JobPostingJob 정보를 가져오는 함수"""
    posting_job = db.query(JobPostingJob).filter(and_(JobPostingJob.poster_id == poster_id_input, JobPostingJob.job_code == job_code_input)).first()
    if posting_job:
        return {"success": True, "job_posting_job": posting_job.to_dict()}
    else:
        return {"success": False, "message": "JobPostingJob not found"}

def delete_job_posting_job(db: Session, poster_id_input: str, job_code_input: int) -> dict:
    """기존 JobPostingJob 정보를 삭제하는 함수"""
    posting_job = db.query(JobPostingJob).filter(and_(JobPostingJob.poster_id == poster_id_input, JobPostingJob.job_code == job_code_input)).first()
    if posting_job:
        try:
            db.delete(posting_job)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "JobPostingJob not found"}