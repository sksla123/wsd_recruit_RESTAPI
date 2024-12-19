# models/loc_code.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

from . import Base

class LocCode(Base):
    """
    LocCode 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "LocCode"

    loc_code = Column(Integer, primary_key=True)
    loc_name = Column(String(255), nullable=False)
    loc_mcode = Column(Integer)
    loc_mname = Column(String(255))

    def to_dict(self):
        return {
            "loc_code": self.loc_code,
            "loc_name": self.loc_name,
            "loc_mcode": self.loc_mcode,
            "loc_mname": self.loc_mname
        }

def get_loc_codes(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """
    LocCode 목록을 조회하는 함수 (Pagination 적용)
    """
    try:
        offset = (page - 1) * item_counts
        loc_codes = db.query(LocCode).offset(offset).limit(item_counts).all()
        total_count = db.query(LocCode).count()
        data = {
            "loc_codes": [loc_code.to_dict() for loc_code in loc_codes],
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
            "message": "Fail to load Location Table",
        }

def create_loc_code(db: Session, loc_code: int, loc_name: str, loc_mcode: int = None, loc_mname: str = None) -> dict:
    """
    새로운 LocCode를 생성하는 함수
    """
    try:
        new_loc_code = LocCode(loc_code=loc_code, loc_name=loc_name, loc_mcode=loc_mcode, loc_mname=loc_mname)
        db.add(new_loc_code)
        db.commit()
        db.refresh(new_loc_code)
        return {"success": True, "loc_code": new_loc_code.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_loc_code_by_id(db: Session, loc_code_id: int) -> dict:
    """
    loc_code로 LocCode 정보를 가져오는 함수
    """
    loc_code = db.query(LocCode).filter(LocCode.loc_code == loc_code_id).first()
    if loc_code:
        return {"success": True, "loc_code": loc_code.to_dict()}
    else:
        return {"success": False, "message": "LocCode not found"}

def update_loc_code(db: Session, loc_code_id: int, new_loc_name: str = None, new_loc_mcode: int = None, new_loc_mname: str = None) -> dict:
    """
    기존 LocCode 정보를 수정하는 함수
    """
    loc_code = db.query(LocCode).filter(LocCode.loc_code == loc_code_id).first()
    if loc_code:
        try:
            if new_loc_name is not None: loc_code.loc_name = new_loc_name
            if new_loc_mcode is not None: loc_code.loc_mcode = new_loc_mcode
            if new_loc_mname is not None: loc_code.loc_mname = new_loc_mname
            db.commit()
            return {"success": True, "loc_code": loc_code.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "LocCode not found"}

def delete_loc_code(db: Session, loc_code_id: int) -> dict:
    """
    기존 LocCode 정보를 삭제하는 함수
    """
    loc_code = db.query(LocCode).filter(LocCode.loc_code == loc_code_id).first()
    if loc_code:
        try:
            db.delete(loc_code)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "LocCode not found"}