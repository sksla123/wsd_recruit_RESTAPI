# models/company_group.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from . import Base

class CompanyGroup(Base):
    """
    CompanyGroup 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "CompanyGroup"

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255))

    companies = relationship("Company", back_populates="group", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "group_id": self.group_id,
            "group_name": self.group_name
        }

def get_company_groups(db: Session, page: int = 1, item_counts: int = 20) -> dict:
    """
    CompanyGroup 목록을 조회하는 함수 (Pagination 적용)
    """
    offset = (page - 1) * item_counts
    groups = db.query(CompanyGroup).offset(offset).limit(item_counts).all()
    total_count = db.query(CompanyGroup).count()
    return {
        "groups": [group.to_dict() for group in groups],
        "total_count": total_count,
        "current_page": page,
        "total_page": (total_count + item_counts - 1) // item_counts # 총 페이지 수 계산
    }

def create_company_group(db: Session, group_name: str) -> dict:
    """
    새로운 CompanyGroup을 생성하는 함수
    """
    try:
        new_group = CompanyGroup(group_name=group_name)
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return {"success": True, "group": new_group.to_dict()}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
        
def get_company_group_by_id(db: Session, group_id: int) -> dict:
    """
    group_id로 CompanyGroup 정보를 가져오는 함수
    """
    group = db.query(CompanyGroup).filter(CompanyGroup.group_id == group_id).first()
    if group:
        return {"success": True, "group": group.to_dict()}
    else:
        return {"success": False, "message": "Group not found"}

def update_company_group(db: Session, group_id: int, new_group_name: str) -> dict:
    """
    기존 CompanyGroup 정보를 수정하는 함수
    """
    group = db.query(CompanyGroup).filter(CompanyGroup.group_id == group_id).first()
    if group:
        try:
            group.group_name = new_group_name
            db.commit()
            return {"success": True, "group": group.to_dict()}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "Group not found"}

def delete_company_group(db: Session, group_id: int) -> dict:
    """
    기존 CompanyGroup 정보를 삭제하는 함수
    """
    group = db.query(CompanyGroup).filter(CompanyGroup.group_id == group_id).first()
    if group:
        try:
            db.delete(group)
            db.commit()
            return {"success": True}
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    else:
        return {"success": False, "message": "Group not found"}
    