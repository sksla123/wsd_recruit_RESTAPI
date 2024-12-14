# models/job_posting.py
from sqlalchemy import Column, String, Integer, Date, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError
from datetime import date

Base = declarative_base()

class JobPosting(Base):
    """
    JobPosting 테이블 모델

    Attributes:
        comp_id (int): 회사 ID (FK)
        poster_id (str): 공고 ID (PK)
        poster_title (str): 공고 제목 (NN)
        poster_link (str): 공고 링크
        job_sectors (JSON): 직무 분야 (JSON)
        job_career (str): 경력 조건
        job_education (str): 학력 조건
        edu_code (int): 학력 코드 (FK)
        edu_upper (int or None): 상위 학력 코드
        deadline_date (date): 마감일 (NN)
        last_updated_date (date): 최종 수정일 (NN)
        job_codes (JSON): 직무 코드 목록 (JSON)
        loc_codes (JSON): 지역 코드 목록 (JSON)
        sal_code (int): 급여 코드 (FK)
        poster_status (int): 공고 상태
        poster_writer_user_id (str): 공고 작성자 ID (FK)
    """
    __tablename__ = 'JobPosting'

    comp_id = Column(Integer, ForeignKey('Company.comp_id'), nullable=False, comment="회사 ID")
    poster_id = Column(String(255), primary_key=True, comment="공고 ID")
    poster_title = Column(String(255), nullable=False, comment="공고 제목")
    poster_link = Column(String(255), comment="공고 링크")
    job_sectors = Column(JSON, comment="직무 분야")
    job_career = Column(String(255), comment="경력 조건")
    job_education = Column(String(255), comment="학력 조건")
    edu_code = Column(Integer, ForeignKey('EduCode.edu_code'), nullable=False, comment="학력 코드")
    edu_upper = Column(Integer, comment="상위 학력 코드")
    deadline_date = Column(Date, nullable=False, comment="마감일")
    last_updated_date = Column(Date, nullable=False, default=date.today, onupdate=date.today, comment="최종 수정일")
    job_codes = Column(JSON, nullable=False, comment="직무 코드 목록")
    loc_codes = Column(JSON, nullable=False, comment="지역 코드 목록")
    sal_code = Column(Integer, ForeignKey('SalCode.sal_code'), nullable=False, comment="급여 코드")
    poster_status = Column(Integer, nullable=False, comment="공고 상태")
    poster_writer_user_id = Column(String(255), ForeignKey('User.user_id'), nullable=False, comment="공고 작성자 ID")

    def to_dict(self):
      return {
          "comp_id": self.comp_id,
          "poster_id": self.poster_id,
          "poster_title": self.poster_title,
          "poster_link": self.poster_link,
          "job_sectors": self.job_sectors,
          "job_career": self.job_career,
          "job_education": self.job_education,
          "edu_code": self.edu_code,
          "edu_upper": self.edu_upper,
          "deadline_date": self.deadline_date.isoformat() if self.deadline_date else None,
          "last_updated_date": self.last_updated_date.isoformat() if self.last_updated_date else None,
          "job_codes": self.job_codes,
          "loc_codes": self.loc_codes,
          "sal_code": self.sal_code,
          "poster_status": self.poster_status,
          "poster_writer_user_id": self.poster_writer_user_id
      }

def create_job_posting(db: Session, comp_id: int, poster_id: str, poster_title: str, poster_link: str, job_sectors: list, job_career: str, job_education: str, edu_code: int, edu_upper: int, deadline_date: date, job_codes: list, loc_codes: list, sal_code: int, poster_status: int, poster_writer_user_id: str):
    """새로운 JobPosting 레코드 생성"""
    try:
        db_job_posting = JobPosting(comp_id=comp_id, poster_id=poster_id, poster_title=poster_title, poster_link=poster_link, job_sectors=job_sectors, job_career=job_career, job_education=job_education, edu_code=edu_code, edu_upper=edu_upper, deadline_date=deadline_date, job_codes=job_codes, loc_codes=loc_codes, sal_code=sal_code, poster_status=poster_status, poster_writer_user_id=poster_writer_user_id)
        db.add(db_job_posting)
        db.commit()
        db.refresh(db_job_posting)
        return db_job_posting.to_dict(), "공고가 성공적으로 생성되었습니다."
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e):
            return None, "이미 존재하는 공고 ID입니다."
        return None, f"데이터베이스 무결성 오류: {str(e)}"
    except Exception as e:
        db.rollback()
        return None, f"공고 생성 중 오류가 발생했습니다: {str(e)}"

def get_job_posting(db: Session, poster_id: str):
    """poster_id로 JobPosting 레코드 조회"""
    try:
        job_posting_obj = db.query(JobPosting).filter(JobPosting.poster_id == poster_id).first()
        if job_posting_obj:
            return job_posting_obj.to_dict(), "공고 조회 성공"
        return None, "해당하는 공고가 없습니다."
    except Exception as e:
        return None, f"공고 조회 중 오류가 발생했습니다: {str(e)}"

def get_job_posting_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """JobPosting 레코드 목록 조회 (페이지네이션 지원)"""
    try:
        query = db.query(JobPosting)
        if pagination:
            job_postings = query.offset((page - 1) * per_page).limit(per_page).all()
        else:
            job_postings = query.all()
        job_posting_list = [job_posting.to_dict() for job_posting in job_postings]
        return job_posting_list, "공고 목록 조회 성공"
    except Exception as e:
        return None, f"공고 목록 조회 중 오류가 발생했습니다: {str(e)}"
    
def update_job_posting(db: Session, poster_id: str, comp_id: int = None, poster_title: str = None, poster_link: str = None, job_sectors: list = None, job_career: str = None, job_education: str = None, edu_code: int = None, edu_upper: int = None, deadline_date: date = None, job_codes: list = None, loc_codes: list = None, sal_code: int = None, poster_status: int = None):
    """
    JobPosting 레코드 업데이트

    Args:
        db (Session): 데이터베이스 세션
        poster_id (str): 수정할 공고 ID (필수)
        comp_id (int, optional): 회사 ID
        poster_title (str, optional): 공고 제목
        poster_link (str, optional): 공고 링크
        job_sectors (list, optional): 직무 분야
        job_career (str, optional): 경력 조건
        job_education (str, optional): 학력 조건
        edu_code (int, optional): 학력 코드
        edu_upper (int, optional): 상위 학력 코드
        deadline_date (date, optional): 마감일
        job_codes (list, optional): 직무 코드 목록
        loc_codes (list, optional): 지역 코드 목록
        sal_code (int, optional): 급여 코드
        poster_status (int, optional): 공고 상태

    Returns:
        tuple: (dict, str) - (업데이트된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        job_posting_obj = db.query(JobPosting).filter(JobPosting.poster_id == poster_id).first()
        if job_posting_obj:
            if comp_id is not None: job_posting_obj.comp_id = comp_id
            if poster_title is not None: job_posting_obj.poster_title = poster_title
            if poster_link is not None: job_posting_obj.poster_link = poster_link
            if job_sectors is not None: job_posting_obj.job_sectors = job_sectors
            if job_career is not None: job_posting_obj.job_career = job_career
            if job_education is not None: job_posting_obj.job_education = job_education
            if edu_code is not None: job_posting_obj.edu_code = edu_code
            if edu_upper is not None: job_posting_obj.edu_upper = edu_upper
            if deadline_date is not None: job_posting_obj.deadline_date = deadline_date
            if job_codes is not None: job_posting_obj.job_codes = job_codes
            if loc_codes is not None: job_posting_obj.loc_codes = loc_codes
            if sal_code is not None: job_posting_obj.sal_code = sal_code
            if poster_status is not None: job_posting_obj.poster_status = poster_status
            db.commit()
            db.refresh(job_posting_obj)
            return job_posting_obj.to_dict(), "공고가 성공적으로 수정되었습니다."
        return None, "해당하는 공고가 없습니다."
    except IntegrityError as e:
        db.rollback()
        return None, f"데이터베이스 무결성 오류: {str(e)}"
    except Exception as e:
        db.rollback()
        return None, f"공고 수정 중 오류가 발생했습니다: {str(e)}"

def delete_job_posting(db: Session, poster_id: str):
    """
    JobPosting 레코드 삭제

    Args:
        db (Session): 데이터베이스 세션
        poster_id (str): 삭제할 공고 ID

    Returns:
        tuple: (None, str) - (None, 메시지)
    """
    try:
        job_posting_obj = db.query(JobPosting).filter(JobPosting.poster_id == poster_id).first()
        if job_posting_obj:
            db.delete(job_posting_obj)
            db.commit()
            return None, "공고가 성공적으로 삭제되었습니다."
        return None, "해당하는 공고가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"공고 삭제 중 오류가 발생했습니다: {str(e)}"