# models/sal_code.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

class SalCode(Base):
    """
    SalCode 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "SalCode"

    sal_code = Column(Integer, primary_key=True)
    sal_name = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "sal_code": self.sal_code,
            "sal_name": self.sal_name
        }

def get_sal_codes(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """
    SalCode 목록을 조회하는 함수 (Pagination 적용)
    """
    offset = (page - 1) * item_counts
    sal_codes = db.query(SalCode).offset(offset).limit(item_counts).all()
    total_count = db.query(SalCode).count()
    return {
        "sal_codes": [sal_code.to_dict() for sal_code in sal_codes],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_sal_code(db: Session, sal_code: int, sal_name: str) -> dict:
    """
    새로운 SalCode를 생성하는 함수
    """
    try:
        new_sal_code = SalCode(sal_code=sal_code, sal_name=sal_name)
        db.add(new_sal_code)
        db.commit()
        db.refresh(new_sal_code)
        return {"success": True, "sal_code": new_sal_code.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_sal_code_by_id(db: Session, sal_code_id: int) -> dict: #인자 이름 수정
    """
    sal_code로 SalCode 정보를 가져오는 함수
    """
    sal_code = db.query(SalCode).filter(SalCode.sal_code == sal_code_id).first() #필터 조건 수정
    if sal_code:
        return {"success": True, "sal_code": sal_code.to_dict()}
    else:
        return {"success": False, "message": "SalCode not found"}

def update_sal_code(db: Session, sal_code_id: int, new_sal_name: str) -> dict: #인자 이름 수정
    """
    기존 SalCode 정보를 수정하는 함수
    """
    sal_code = db.query(SalCode).filter(SalCode.sal_code == sal_code_id).first() #필터 조건 수정
    if sal_code:
        try:
            sal_code.sal_name = new_sal_name
            db.commit()
            return {"success": True, "sal_code": sal_code.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "SalCode not found"}

def delete_sal_code(db: Session, sal_code_id: int) -> dict: #인자 이름 수정
    """
    기존 SalCode 정보를 삭제하는 함수
    """
    sal_code = db.query(SalCode).filter(SalCode.sal_code == sal_code_id).first() #필터 조건 수정
    if sal_code:
        try:
            db.delete(sal_code)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "SalCode not found"}