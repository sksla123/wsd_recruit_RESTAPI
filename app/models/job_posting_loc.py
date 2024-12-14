# models/job_posting_loc.py
from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class JobPostingLoc(Base):
    """
    JobPostingLoc 테이블 모델 (JobPosting과 LocCode 간의 다대다 관계 연결 테이블)

    Attributes:
        poster_id (str): 공고 ID (FK, JobPosting 테이블 참조)
        loc_code (int): 지역 코드 (FK, LocCode 테이블 참조)
    """
    __tablename__ = 'JobPostingLoc'

    poster_id = Column(String(255), ForeignKey('JobPosting.poster_id'), primary_key=True, comment="공고 ID")
    loc_code = Column(Integer, ForeignKey('LocCode.loc_code'), primary_key=True, comment="지역 코드")

    __table_args__ = (
        PrimaryKeyConstraint('poster_id', 'loc_code'),  # 복합 기본 키 설정
    )

    def to_dict(self):
        return {
            "poster_id": self.poster_id,
            "loc_code": self.loc_code
        }

def create_job_posting_loc(db: Session, poster_id: str, loc_code: int):
    """새로운 JobPostingLoc 레코드 생성"""
    try:
        db_job_posting_loc = JobPostingLoc(poster_id=poster_id, loc_code=loc_code)
        db.add(db_job_posting_loc)
        db.commit()
        db.refresh(db_job_posting_loc)
        return db_job_posting_loc.to_dict(), "채용 공고-지역 연결이 성공적으로 생성되었습니다."
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e):
            return None, "이미 존재하는 채용 공고-지역 연결입니다."
        return None, f"데이터베이스 무결성 오류(FK 제약 조건 위반): {str(e)}" #외래 키 제약조건 등
    except Exception as e:
        db.rollback()
        return None, f"채용 공고-지역 연결 생성 중 오류가 발생했습니다: {str(e)}"

def get_job_posting_loc(db: Session, poster_id: str, loc_code: int):
    """poster_id와 loc_code로 JobPostingLoc 레코드 조회"""
    try:
        job_posting_loc_obj = db.query(JobPostingLoc).filter(JobPostingLoc.poster_id == poster_id, JobPostingLoc.loc_code == loc_code).first()
        if job_posting_loc_obj:
            return job_posting_loc_obj.to_dict(), "채용 공고-지역 연결 조회 성공"
        return None, "해당하는 채용 공고-지역 연결이 없습니다."
    except Exception as e:
        return None, f"채용 공고-지역 연결 조회 중 오류가 발생했습니다: {str(e)}"

def get_job_posting_loc_list_by_poster_id(db: Session, poster_id: str):
    """poster_id로 JobPostingLoc 레코드 목록 조회"""
    try:
        job_posting_loc_list = db.query(JobPostingLoc).filter(JobPostingLoc.poster_id == poster_id).all()
        if job_posting_loc_list:
            result = [job_posting_loc.to_dict() for job_posting_loc in job_posting_loc_list]
            return result, f"해당 poster_id({poster_id})의 채용 공고-지역 목록 조회 성공"
        return None, f"해당 poster_id({poster_id})에 연결된 지역이 없습니다."
    except Exception as e:
        return None, f"채용 공고-지역 목록 조회 중 오류가 발생했습니다: {str(e)}"

def get_job_posting_loc_list_by_loc_code(db: Session, loc_code: int):
    """loc_code로 JobPostingLoc 레코드 목록 조회"""
    try:
        job_posting_loc_list = db.query(JobPostingLoc).filter(JobPostingLoc.loc_code == loc_code).all()
        if job_posting_loc_list:
            result = [job_posting_loc.to_dict() for job_posting_loc in job_posting_loc_list]
            return result, f"해당 loc_code({loc_code})의 채용 공고 목록 조회 성공"
        return None, f"해당 loc_code({loc_code})에 연결된 채용 공고가 없습니다."
    except Exception as e:
        return None, f"채용 공고 목록 조회 중 오류가 발생했습니다: {str(e)}"

def delete_job_posting_loc(db: Session, poster_id: str, loc_code: int):
    """JobPostingLoc 레코드 삭제"""
    try:
        job_posting_loc_obj = db.query(JobPostingLoc).filter(JobPostingLoc.poster_id == poster_id, JobPostingLoc.loc_code == loc_code).first()
        if job_posting_loc_obj:
            db.delete(job_posting_loc_obj)
            db.commit()
            return None, "채용 공고-지역 연결이 성공적으로 삭제되었습니다."
        return None, "해당하는 채용 공고-지역 연결이 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"채용 공고-지역 연결 삭제 중 오류가 발생했습니다: {str(e)}"

def delete_job_posting_loc_by_poster_id(db: Session, poster_id: str):
    """poster_id로 JobPostingLoc 레코드 일괄 삭제"""
    try:
        delete_count = db.query(JobPostingLoc).filter(JobPostingLoc.poster_id == poster_id).delete()
        db.commit()
        return None, f"poster_id({poster_id})에 연결된 {delete_count}개의 지역 연결이 삭제되었습니다."
    except Exception as e:
        db.rollback()
        return None, f"채용 공고-지역 일괄 삭제 중 오류가 발생했습니다: {str(e)}"

def delete_job_posting_loc_by_loc_code(db: Session, loc_code: int):
    """loc_code로 JobPostingLoc 레코드 일괄 삭제"""
    try:
        delete_count = db.query(JobPostingLoc).filter(JobPostingLoc.loc_code == loc_code).delete()
        db.commit()
        return None, f"loc_code({loc_code})에 연결된 {delete_count}개의 채용 공고 연결이 삭제되었습니다."
    except Exception as e:
        db.rollback()
        return None, f"채용 공고-지역 일괄 삭제 중 오류가 발생했습니다: {str(e)}"