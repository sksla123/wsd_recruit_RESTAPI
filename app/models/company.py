# models/company.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session

from .database import Base

class Company(Base):
    """
    Company 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "Company"

    comp_id = Column(Integer, primary_key=True, autoincrement=True)
    comp_name = Column(String(255), nullable=False)
    comp_link = Column(String(255))
    group_id = Column(Integer, ForeignKey("CompanyGroup.group_id"), nullable=True)

    # group = relationship("CompanyGroup", back_populates="companies") # CompanyGroup 과의 관계 설정

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
    
if __name__ == "__main__":
    from .database import engine, SessionLocal
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. create_company 테스트
        result_create = create_company(db, "테스트 회사1", "https://test.com", None)
        assert result_create["success"], f"create_company 실패: {result_create.get('error')}"
        created_company = result_create["company"]
        print("create_company 테스트 성공")

        # 2. get_company_by_id 테스트
        result_get_by_id = get_company_by_id(db, created_company["comp_id"])
        assert result_get_by_id["success"], f"get_company_by_id 실패: {result_get_by_id.get('message')}"
        retrieved_company = result_get_by_id["company"]
        assert created_company["comp_name"] == retrieved_company["comp_name"], "get_company_by_id 데이터 불일치"
        print("get_company_by_id 테스트 성공")
        
        # 3. update_company 테스트
        new_comp_name = "수정된 테스트 회사"
        new_comp_link = "https://updated.test.com"
        result_update = update_company(db, created_company["comp_id"], new_comp_name, new_comp_link, None)
        assert result_update["success"], f"update_company 실패: {result_update.get('error')}"
        updated_company = result_update["company"]
        assert updated_company["comp_name"] == new_comp_name, "update_company comp_name 업데이트 실패"
        assert updated_company["comp_link"] == new_comp_link, "update_company comp_link 업데이트 실패"
        print("update_company 테스트 성공")

        # 4. get_companies 테스트 (pagination 테스트 포함)
        create_company(db, "테스트 회사2", "https://test2.com", None)
        create_company(db, "테스트 회사3", "https://test3.com", None)
        result_get_companies = get_companies(db, page=1, item_counts=2)
        assert len(result_get_companies["companies"]) <= 2, "get_companies 페이지네이션 실패"
        assert result_get_companies["total_count"] == 3, "get_companies 전체 개수 오류"
        print("get_companies 테스트 성공")

        # 5. delete_company 테스트
        result_delete = delete_company(db, created_company["comp_id"])
        assert result_delete["success"], f"delete_company 실패: {result_delete.get('error')}"
        result_get_deleted = get_company_by_id(db, created_company["comp_id"])
        assert not result_get_deleted["success"], "delete_company 삭제 후에도 조회됨"
        print("delete_company 테스트 성공")

        print("모든 테스트 성공!")

    except AssertionError as e:
        print(f"테스트 실패: {e}")
        db.rollback() # 테스트 실패 시 롤백
    finally:
        db.close()