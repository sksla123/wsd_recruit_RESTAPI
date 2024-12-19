# models/edu_code.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

from . import Base

class EduCode(Base):
    """
    EduCode 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "EduCode"

    edu_code = Column(Integer, primary_key=True)
    edu_name = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "edu_code": self.edu_code,
            "edu_name": self.edu_name
        }

def get_edu_codes(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """
    EduCode 목록을 조회하는 함수 (Pagination 적용)
    """
    try:
        offset = (page - 1) * item_counts
        edu_codes = db.query(EduCode).offset(offset).limit(item_counts).all()
        total_count = db.query(EduCode).count()
        data = {
            "edu_codes": [edu_code.to_dict() for edu_code in edu_codes],
            "total_count": total_count,
            "current_page": page,
            "total_page": (total_count + item_counts - 1) // item_counts
        }
        return {
            "success": True,
            "data": data,
        }
    except Exception as e:
        return {
            "success": False,
            "data": {},
            "message": "Fail to load Education Table",
        }


def create_edu_code(db: Session, edu_code: int, edu_name: str) -> dict:
    """
    새로운 EduCode를 생성하는 함수
    """
    try:
        new_edu_code = EduCode(edu_code=edu_code, edu_name=edu_name)
        db.add(new_edu_code)
        db.commit()
        db.refresh(new_edu_code)
        return {"success": True, "edu_code": new_edu_code.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_edu_code_by_id(db: Session, edu_code_id: int) -> dict: # 인자 이름 통일
    """
    edu_code로 EduCode 정보를 가져오는 함수
    """
    edu_code = db.query(EduCode).filter(EduCode.edu_code == edu_code_id).first()
    if edu_code:
        return {"success": True, "edu_code": edu_code.to_dict()}
    else:
        return {"success": False, "message": "EduCode not found"}

def update_edu_code(db: Session, edu_code_id: int, new_edu_name: str) -> dict: # 인자 이름 통일
    """
    기존 EduCode 정보를 수정하는 함수
    """
    edu_code = db.query(EduCode).filter(EduCode.edu_code == edu_code_id).first()
    if edu_code:
        try:
            edu_code.edu_name = new_edu_name
            db.commit()
            return {"success": True, "edu_code": edu_code.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "EduCode not found"}

def delete_edu_code(db: Session, edu_code_id: int) -> dict: # 인자 이름 통일
    """
    기존 EduCode 정보를 삭제하는 함수
    """
    edu_code = db.query(EduCode).filter(EduCode.edu_code == edu_code_id).first()
    if edu_code:
        try:
            db.delete(edu_code)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "EduCode not found"}