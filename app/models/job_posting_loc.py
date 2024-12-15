# models/job_posting_loc.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import and_

from . import Base

class JobPostingLoc(Base):
    """JobPostingLoc 테이블에 대한 SQLAlchemy 모델 클래스"""
    __tablename__ = "JobPostingLoc"

    poster_id = Column(String(255), ForeignKey("JobPosting.poster_id"), primary_key=True, nullable=False)
    loc_code = Column(Integer, ForeignKey("LocCode.loc_code"), primary_key=True, nullable=False)

    # job_posting = relationship("JobPosting", back_populates="job_posting_locs")
    # loc_code_info = relationship("LocCode", back_populates="job_posting_locs")

    def to_dict(self):
        """JobPostingLoc 객체를 딕셔너리로 변환합니다."""
        return {
            "poster_id": self.poster_id,
            "loc_code": self.loc_code
        }

def get_job_posting_locs(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """JobPostingLoc 목록을 조회하는 함수 (Pagination 적용)"""
    offset = (page - 1) * item_counts
    total_count = db.query(JobPostingLoc).count()
    locs = db.query(JobPostingLoc).offset(offset).limit(item_counts).all()
    return {
        "success": True,
        "job_posting_locs": [loc.to_dict() for loc in locs],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_job_posting_loc(db: Session, poster_id: str, loc_code: int) -> dict:
    """새로운 JobPostingLoc을 생성하는 함수"""
    try:
        new_posting_loc = JobPostingLoc(poster_id=poster_id, loc_code=loc_code)
        db.add(new_posting_loc)
        db.commit()
        db.refresh(new_posting_loc)
        return {"success": True, "job_posting_loc": new_posting_loc.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_job_posting_loc_by_ids(db: Session, poster_id_input: str, loc_code_input: int) -> dict:
    """poster_id와 loc_code로 JobPostingLoc 정보를 가져오는 함수"""
    posting_loc = db.query(JobPostingLoc).filter(and_(JobPostingLoc.poster_id == poster_id_input, JobPostingLoc.loc_code == loc_code_input)).first()
    if posting_loc:
        return {"success": True, "job_posting_loc": posting_loc.to_dict()}
    else:
        return {"success": False, "message": "JobPostingLoc not found"}

def delete_job_posting_loc(db: Session, poster_id_input: str, loc_code_input: int) -> dict:
    """기존 JobPostingLoc 정보를 삭제하는 함수"""
    posting_loc = db.query(JobPostingLoc).filter(and_(JobPostingLoc.poster_id == poster_id_input, JobPostingLoc.loc_code == loc_code_input)).first()
    if posting_loc:
        try:
            db.delete(posting_loc)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "JobPostingLoc not found"}