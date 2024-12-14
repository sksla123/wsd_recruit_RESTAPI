# models/job_posting_job.py
from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class JobPostingJob(Base):
    """
    JobPostingJob 테이블 모델 (JobPosting과 JobCode 간의 다대다 관계 연결 테이블)

    Attributes:
        poster_id (str): 공고 ID (FK, JobPosting 테이블 참조)
        job_code (int): 직무 코드 (FK, JobCode 테이블 참조)
    """
    __tablename__ = 'JobPostingJob'

    poster_id = Column(String(255), ForeignKey('JobPosting.poster_id'), primary_key=True, comment="공고 ID")
    job_code = Column(Integer, ForeignKey('JobCode.job_code'), primary_key=True, comment="직무 코드")

    __table_args__ = (
        PrimaryKeyConstraint('poster_id', 'job_code'),  # 복합 기본 키 설정
    )

    def to_dict(self):
        return {
            "poster_id": self.poster_id,
            "job_code": self.job_code
        }

def create_job_posting_job(db: Session, poster_id: str, job_code: int):
    """새로운 JobPostingJob 레코드 생성"""
    try:
        db_job_posting_job = JobPostingJob(poster_id=poster_id, job_code=job_code)
        db.add(db_job_posting_job)
        db.commit()
        db.refresh(db_job_posting_job)
        return db_job_posting_job.to_dict(), "채용 공고-직무 연결이 성공적으로 생성되었습니다."
    except IntegrityError as e: #이미 존재하는 조합이거나, FK제약조건에 위배되는 경우 발생
        db.rollback()
        if "Duplicate entry" in str(e): #중복된 데이터 삽입 시
            return None, "이미 존재하는 채용 공고-직무 연결입니다."
        return None, f"데이터베이스 무결성 오류(FK 제약 조건 위반): {str(e)}"
    except Exception as e:
        db.rollback()
        return None, f"채용 공고-직무 연결 생성 중 오류가 발생했습니다: {str(e)}"

def get_job_posting_job(db: Session, poster_id: str, job_code: int):
    """poster_id와 job_code로 JobPostingJob 레코드 조회"""
    try:
        job_posting_job_obj = db.query(JobPostingJob).filter(JobPostingJob.poster_id == poster_id, JobPostingJob.job_code == job_code).first()
        if job_posting_job_obj:
            return job_posting_job_obj.to_dict(), "채용 공고-직무 연결 조회 성공"
        return None, "해당하는 채용 공고-직무 연결이 없습니다."
    except Exception as e:
        return None, f"채용 공고-직무 연결 조회 중 오류가 발생했습니다: {str(e)}"

def get_job_posting_job_list_by_poster_id(db: Session, poster_id: str):
    """poster_id로 JobPostingJob 레코드 목록 조회"""
    try:
        job_posting_job_list = db.query(JobPostingJob).filter(JobPostingJob.poster_id == poster_id).all()
        if job_posting_job_list:
            result = [job_posting_job.to_dict() for job_posting_job in job_posting_job_list]
            return result, f"해당 poster_id({poster_id})의 채용 공고-직무 목록 조회 성공"
        return None, f"해당 poster_id({poster_id})에 연결된 직무가 없습니다."
    except Exception as e:
        return None, f"채용 공고-직무 목록 조회 중 오류가 발생했습니다: {str(e)}"

def get_job_posting_job_list_by_job_code(db: Session, job_code: int):
    """job_code로 JobPostingJob 레코드 목록 조회"""
    try:
        job_posting_job_list = db.query(JobPostingJob).filter(JobPostingJob.job_code == job_code).all()
        if job_posting_job_list:
            result = [job_posting_job.to_dict() for job_posting_job in job_posting_job_list]
            return result, f"해당 job_code({job_code})의 채용 공고 목록 조회 성공"
        return None, f"해당 job_code({job_code})에 연결된 채용 공고가 없습니다."
    except Exception as e:
        return None, f"채용 공고 목록 조회 중 오류가 발생했습니다: {str(e)}"

def delete_job_posting_job(db: Session, poster_id: str, job_code: int):
    """JobPostingJob 레코드 삭제"""
    try:
        job_posting_job_obj = db.query(JobPostingJob).filter(JobPostingJob.poster_id == poster_id, JobPostingJob.job_code == job_code).first()
        if job_posting_job_obj:
            db.delete(job_posting_job_obj)
            db.commit()
            return None, "채용 공고-직무 연결이 성공적으로 삭제되었습니다."
        return None, "해당하는 채용 공고-직무 연결이 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"채용 공고-직무 연결 삭제 중 오류가 발생했습니다: {str(e)}"

def delete_job_posting_job_by_poster_id(db: Session, poster_id: str):
    """poster_id로 JobPostingJob 레코드 일괄 삭제"""
    try:
        delete_count = db.query(JobPostingJob).filter(JobPostingJob.poster_id == poster_id).delete()
        db.commit()
        return None, f"poster_id({poster_id})에 연결된 {delete_count}개의 직무 연결이 삭제되었습니다."
    except Exception as e:
        db.rollback()
        return None, f"채용 공고-직무 일괄 삭제 중 오류가 발생했습니다: {str(e)}"

def delete_job_posting_job_by_job_code(db: Session, job_code: int):
    """job_code로 JobPostingJob 레코드 일괄 삭제"""
    try:
        delete_count = db.query(JobPostingJob).filter(JobPostingJob.job_code == job_code).delete()
        db.commit()
        return None, f"job_code({job_code})에 연결된 {delete_count}개의 채용 공고 연결이 삭제되었습니다."
    except Exception as e:
        db.rollback()
        return None, f"채용 공고-직무 일괄 삭제 중 오류가 발생했습니다: {str(e)}"