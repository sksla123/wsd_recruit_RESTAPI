from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, JSON, asc, desc, and_, or_
from sqlalchemy.orm import declarative_base, relationship, Session
from datetime import date
from typing import Optional

Base = declarative_base()

class JobPosting(Base):
    """JobPosting 테이블에 대한 SQLAlchemy 모델 클래스"""
    __tablename__ = "JobPosting"

    comp_id = Column(Integer, ForeignKey("Company.comp_id"), nullable=False)
    poster_id = Column(String(255), primary_key=True, nullable=False)
    poster_title = Column(String(255), nullable=False)
    poster_link = Column(String(255))
    job_sectors = Column(String(255))
    job_career = Column(String(255))
    job_education = Column(String(255))
    edu_code = Column(Integer, ForeignKey("EduCode.edu_code"), nullable=False)
    edu_upper = Column(Integer)
    deadline_date = Column(Date, nullable=False)
    last_updated_date = Column(Date, nullable=False)
    job_codes = Column(JSON, nullable=False)
    loc_codes = Column(JSON, nullable=False)
    sal_code = Column(Integer, ForeignKey("SalCode.sal_code"), nullable=False)
    poster_status = Column(Integer, nullable=False)
    poster_writer_user_id = Column(String(255), ForeignKey("User.user_id"), nullable=False)

    company = relationship("Company", back_populates="postings")
    edu = relationship("EduCode", back_populates="postings")
    sal = relationship("SalCode", back_populates="postings")
    writer = relationship("User", back_populates="written_postings")

    def to_dict(self):
        """JobPosting 객체를 딕셔너리로 변환"""
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
            "poster_writer_user_id": self.poster_writer_user_id,
        }

# 정렬 로직을 함수로 분리
def _apply_ordering(query, sort_criteria: dict):
    order_by_clauses = []
    for column_name, sort_info in sort_criteria.items():
        column = getattr(JobPosting, column_name, None)
        if column is None:
            raise ValueError(f"Invalid column name: {column_name}")

        sorting_method = sort_info.get('sorting_method', 0)  # 0: asc, 1: desc
        if sorting_method == 0:
            order_by_clauses.append(asc(column))
        elif sorting_method == 1:
            order_by_clauses.append(desc(column))
        else:
            raise ValueError(f"Invalid sorting method for column: {column_name}, Value should be 0 or 1.")
    return query.order_by(*order_by_clauses)


def get_job_postings(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """JobPosting 목록 조회 (Pagination 적용)"""
    try:
        offset = (page - 1) * item_counts
        postings = db.query(JobPosting).offset(offset).limit(item_counts).all()
        total_count = db.query(JobPosting).count()
        return {
            "success": True,
            "postings": [posting.to_dict() for posting in postings],
            "total_count": total_count,
            "current_page": page,
            "total_page": (total_count + item_counts - 1) // item_counts
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_job_postings_sorted_by(db: Session, sort_criteria: dict, page: int = 1, item_counts: int = 20) -> dict:
    """특정 속성으로 정렬된 JobPosting 목록 조회 (Pagination 적용)"""
    try:
        query = db.query(JobPosting)
        query = _apply_ordering(query, sort_criteria)
        offset = (page - 1) * item_counts
        postings = query.offset(offset).limit(item_counts).all()
        total_count = db.query(JobPosting).count()
        return {
           "success": True,
            "postings": [posting.to_dict() for posting in postings],
            "total_count": total_count,
            "current_page": page,
            "total_page": (total_count + item_counts - 1) // item_counts
        }
    except ValueError as e:  # 유효하지 않은 column_name 또는 sorting_method 예외처리
        return {"success": False, "message": str(e)}
    except Exception as e:
       return {"success": False, "message": str(e)}

POSTER_STATUS_ACTIVE = 1
POSTER_STATUS_EXTENDED = 0
POSTER_STATUS_INACTIVE = 2

def get_available_job_postings_sorted_by(db: Session, sort_criteria: dict, page: int = 1, item_counts: int = 20) -> dict:
    """마감일자가 지나지 않았거나, 지났더라도 무기한 연장된 JobPosting 목록 정렬 조회"""
    try:
        query = db.query(JobPosting).filter(
            and_(
                JobPosting.poster_status < POSTER_STATUS_INACTIVE,
                or_(
                    JobPosting.poster_status == POSTER_STATUS_EXTENDED,
                    JobPosting.deadline_date >= date.today()
                    )
            )
        )
        query = _apply_ordering(query, sort_criteria)
        offset = (page - 1) * item_counts
        postings = query.offset(offset).limit(item_counts).all()
        total_count = query.count()

        return {
           "success": True,
            "postings": [posting.to_dict() for posting in postings],
            "total_count": total_count,
            "current_page": page,
            "total_page": (total_count + item_counts - 1) // item_counts
        }
    except ValueError as e:
        return {"success": False, "message": str(e)}
    except Exception as e:
        return {"success": False, "message": str(e)}

def create_job_posting(db: Session, comp_id: int, poster_id: str, poster_title: str, poster_link: Optional[str] = None, job_sectors: Optional[str] = None, job_career: Optional[str] = None, job_education: Optional[str] = None, edu_code: int = None, edu_upper: Optional[int] = None, deadline_date: Optional[date] = None, job_codes: Optional[list] = None, loc_codes: Optional[list] = None, sal_code: int = None, poster_status: int = POSTER_STATUS_ACTIVE, poster_writer_user_id: str = None) -> dict:
    """새로운 JobPosting 생성"""
    try:
        if not all([comp_id, poster_id, poster_title, edu_code, sal_code, poster_writer_user_id]):
            return {"success": False, "message": "필수 입력 항목이 누락되었습니다."}
            
        now = date.today()
        new_posting = JobPosting(
            comp_id=comp_id,
            poster_id=poster_id,
            poster_title=poster_title,
            poster_link=poster_link,
            job_sectors=job_sectors,
            job_career=job_career,
            job_education=job_education,
            edu_code=edu_code,
            edu_upper=edu_upper,
            deadline_date=deadline_date,
            last_updated_date=now,
            job_codes=job_codes,
            loc_codes=loc_codes,
            sal_code=sal_code,
            poster_status=poster_status,
            poster_writer_user_id=poster_writer_user_id
        )
        db.add(new_posting)
        db.commit()
        db.refresh(new_posting)
        return {"success": True, "posting": new_posting.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": str(e)}

def get_job_posting_by_id(db: Session, poster_id_input: str) -> dict:
    """poster_id로 JobPosting 정보 가져오기"""
    try:
        posting = db.query(JobPosting).filter(JobPosting.poster_id == poster_id_input).first()
        if posting:
            return {"success": True, "posting": posting.to_dict()}
        else:
            return {"success": False, "message": "JobPosting을 찾을 수 없습니다."}
    except Exception as e:
        return {"success": False, "message": str(e)}

def update_job_posting(db: Session, poster_id_input: str, new_comp_id: Optional[int] = None, new_poster_title: Optional[str] = None, new_poster_link: Optional[str] = None, new_job_sectors: Optional[str] = None, new_job_career: Optional[str] = None, new_job_education: Optional[str] = None, new_edu_code: Optional[int] = None, new_edu_upper: Optional[int] = None, new_deadline_date: Optional[date] = None, new_job_codes: Optional[list] = None, new_loc_codes: Optional[list] = None, new_sal_code: Optional[int] = None) -> dict:
    """기존 JobPosting 정보 수정"""
    try:
        with db.begin(): # transaction context 사용
            posting = db.query(JobPosting).filter(JobPosting.poster_id == poster_id_input).first()
            if not posting:
                return {"success": False, "message": "JobPosting을 찾을 수 없습니다."}

            if new_comp_id is not None: posting.comp_id = new_comp_id
            if new_poster_title is not None: posting.poster_title = new_poster_title
            if new_poster_link is not None: posting.poster_link = new_poster_link
            if new_job_sectors is not None: posting.job_sectors = new_job_sectors
            if new_job_career is not None: posting.job_career = new_job_career
            if new_job_education is not None: posting.job_education = new_job_education
            if new_edu_code is not None: posting.edu_code = new_edu_code
            if new_edu_upper is not None: posting.edu_upper = new_edu_upper
            if new_deadline_date is not None: posting.deadline_date = new_deadline_date
            if new_job_codes is not None: posting.job_codes = new_job_codes
            if new_loc_codes is not None: posting.loc_codes = new_loc_codes
            if new_sal_code is not None: posting.sal_code = new_sal_code
            posting.last_updated_date = date.today()

        return {"success": True, "posting": posting.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": str(e)}

def delete_job_posting(db: Session, poster_id_input: str) -> dict:
    """기존 JobPosting 정보 삭제"""
    try:
        with db.begin():  # transaction context 사용
            posting = db.query(JobPosting).filter(JobPosting.poster_id == poster_id_input).first()
            if not posting:
                return {"success": False, "message": "JobPosting을 찾을 수 없습니다."}
            db.delete(posting)
        return {"success": True}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": str(e)}