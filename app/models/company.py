# models/company.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from . import Base

class Company(Base):
    """
    Company 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "Company"

    comp_id = Column(Integer, primary_key=True, autoincrement=True)
    comp_name = Column(String(255), nullable=False)
    comp_link = Column(String(255))
    group_id = Column(Integer, ForeignKey("CompanyGroup.group_id"), nullable=True)

    group = relationship("CompanyGroup", back_populates="companies") # CompanyGroup 과의 관계 설정

    def to_dict(self):
        return {
            "comp_id": self.comp_id,
            "comp_name": self.comp_name,
            "comp_link": self.comp_link,
            "group_id": self.group_id,
        }

def get_companies(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """
    Company 목록을 조회하는 함수 (Pagination 적용)
    """
    offset = (page - 1) * item_counts
    companies = db.query(Company).offset(offset).limit(item_counts).all()
    total_count = db.query(Company).count()
    return {
        "companies": [company.to_dict() for company in companies],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts
    }

def create_company(db: Session, comp_name: str, comp_link: str = None, group_id: int = None) -> dict:
    """
    새로운 Company를 생성하는 함수
    """
    try:
        new_company = Company(comp_name=comp_name, comp_link=comp_link, group_id=group_id)
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        return {"success": True, "company": new_company.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

def get_company_by_id(db: Session, comp_id: int) -> dict:
    """
    comp_id로 Company 정보를 가져오는 함수
    """
    company = db.query(Company).filter(Company.comp_id == comp_id).first()
    if company:
        return {"success": True, "company": company.to_dict()}
    else:
        return {"success": False, "message": "Company not found"}

def update_company(db: Session, comp_id: int, new_comp_name: str = None, new_comp_link: str = None, new_group_id : int = None) -> dict:
    """
    기존 Company 정보를 수정하는 함수
    """
    company = db.query(Company).filter(Company.comp_id == comp_id).first()
    if company:
        try:
            if new_comp_name is not None: company.comp_name = new_comp_name
            if new_comp_link is not None: company.comp_link = new_comp_link
            if new_group_id is not None: company.group_id = new_group_id
            db.commit()
            return {"success": True, "company": company.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "Company not found"}

def delete_company(db: Session, comp_id: int) -> dict:
    """
    기존 Company 정보를 삭제하는 함수
    """
    company = db.query(Company).filter(Company.comp_id == comp_id).first()
    if company:
        try:
            db.delete(company)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "Company not found"}