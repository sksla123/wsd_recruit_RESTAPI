# models/company.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Company(Base):
    """
    Company 테이블 모델

    Attributes:
        comp_id (int): 회사 ID (PK)
        comp_name (str): 회사 이름 (NN)
        comp_link (str): 회사 링크
        group_id (int): 소속 그룹 ID (FK, CompanyGroup.group_id)
        group (CompanyGroup): 소속 그룹 (relationship)
    """
    __tablename__ = 'Company'

    comp_id = Column(Integer, primary_key=True, autoincrement=True)
    comp_name = Column(String(255), nullable=False)
    comp_link = Column(String(255))
    group_id = Column(Integer, ForeignKey('CompanyGroup.group_id', ondelete='SET NULL'))

    group = relationship("CompanyGroup", backref="companies")

    def to_dict(self):
        """
        모델 객체를 딕셔너리로 변환

        Returns:
            dict: 모델의 데이터를 담은 딕셔너리
        """
        return {
            "comp_id": self.comp_id,
            "comp_name": self.comp_name,
            "comp_link": self.comp_link,
            "group_id": self.group_id,
            "group_name": self.group.group_name if self.group else None  # 그룹 이름 추가
        }

def create_company(db: Session, comp_name: str, comp_link: str = None, group_id: int = None):
    """새로운 Company 레코드 생성"""
    try:
      db_company = Company(comp_name=comp_name, comp_link=comp_link, group_id = group_id)
      db.add(db_company)
      db.commit()
      db.refresh(db_company)
      return db_company.to_dict(), "회사가 성공적으로 생성되었습니다."
    except IntegrityError:
      db.rollback()
      return None, "이미 존재하는 회사 이름입니다."
    except Exception as e:
        db.rollback()
        return None, f"회사 생성 중 오류가 발생했습니다: {str(e)}"

def get_company(db: Session, comp_id: int):
    """comp_id로 Company 레코드 조회"""
    try:
      company = db.query(Company).filter(Company.comp_id == comp_id).first()
      if company:
        return company.to_dict(), "회사 조회 성공"
      return None, "해당하는 회사가 없습니다."
    except Exception as e:
        return None, f"회사 조회 중 오류가 발생했습니다: {str(e)}"

def get_company_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """Company 레코드 목록 조회 (페이지네이션 지원)"""
    try:
      query = db.query(Company)
      if pagination:
          companies = query.offset((page - 1) * per_page).limit(per_page).all()
      else:
          companies = query.all()
      company_list = [company.to_dict() for company in companies]
      return company_list, "회사 목록 조회 성공"
    except Exception as e:
        return None, f"회사 목록 조회 중 오류가 발생했습니다: {str(e)}"

def update_company(db: Session, comp_id: int, new_comp_name: str = None, new_comp_link: str = None, group_id : int = None):
    """Company 레코드 업데이트"""
    try:
      company = db.query(Company).filter(Company.comp_id == comp_id).first()
      if company:
        if new_comp_name:
          company.comp_name = new_comp_name
        if new_comp_link:
          company.comp_link = new_comp_link
        company.group_id = group_id
        db.commit()
        db.refresh(company)
        return company.to_dict(), "회사가 성공적으로 수정되었습니다."
      return None, "해당하는 회사가 없습니다."
    except IntegrityError:
      db.rollback()
      return None, "이미 존재하는 회사 이름입니다."
    except Exception as e:
        db.rollback()
        return None, f"회사 수정 중 오류가 발생했습니다: {str(e)}"

def delete_company(db: Session, comp_id: int):
    """Company 레코드 삭제"""
    try:
      company = db.query(Company).filter(Company.comp_id == comp_id).first()
      if company:
        db.delete(company)
        db.commit()
        return None, "회사가 성공적으로 삭제되었습니다."
      return None, "해당하는 회사가 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"회사 삭제 중 오류가 발생했습니다: {str(e)}"