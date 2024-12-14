# models/company_group.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

Base = declarative_base()

class CompanyGroup(Base):
    """
    CompanyGroup 테이블 모델

    Attributes:
        group_id (int): 그룹 ID (PK)
        group_name (str): 그룹 이름
    """
    __tablename__ = 'CompanyGroup'

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255))

    def to_dict(self):
        """
        모델 객체를 딕셔너리로 변환

        Returns:
            dict: 모델의 데이터를 담은 딕셔너리
        """
        return {
            "group_id": self.group_id,
            "group_name": self.group_name
        }

def create_company_group(db: Session, group_name: str):
    """
    새로운 CompanyGroup 레코드를 생성

    Args:
        db (Session): 데이터베이스 세션
        group_name (str): 생성할 그룹 이름

    Returns:
        tuple: (dict, str) - (생성된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        db_group = CompanyGroup(group_name=group_name)
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group.to_dict(), "그룹이 성공적으로 생성되었습니다."
    except IntegrityError:
        db.rollback()
        return None, "이미 존재하는 그룹 이름입니다."
    except Exception as e:
        db.rollback()
        return None, f"그룹 생성 중 오류가 발생했습니다: {str(e)}"

def get_company_group(db: Session, group_id: int):
    """
    group_id로 CompanyGroup 레코드 조회

    Args:
        db (Session): 데이터베이스 세션
        group_id (int): 조회할 그룹 ID

    Returns:
        tuple: (dict, str) - (조회된 데이터, 메시지) 또는 (None, 메시지)
    """
    try:
        group = db.query(CompanyGroup).filter(CompanyGroup.group_id == group_id).first()
        if group:
          return group.to_dict(), "그룹 조회 성공"
        return None, "해당하는 그룹이 없습니다."
    except Exception as e:
        return None, f"그룹 조회 중 오류가 발생했습니다: {str(e)}"

def get_company_group_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """
    CompanyGroup 레코드 목록 조회 (페이지네이션 지원)

    Args:
        db (Session): 데이터베이스 세션
        page (int): 페이지 번호 (기본값: 1)
        per_page (int): 페이지당 항목 수 (기본값: 20)
        pagination (bool): 페이지네이션 사용 여부 (기본값: False)

    Returns:
        tuple: (list, str) - (조회된 데이터 목록, 메시지) 또는 (None, 메시지)
    """
    try:
      query = db.query(CompanyGroup)

      if pagination:
          groups = query.offset((page - 1) * per_page).limit(per_page).all()
      else:
          groups = query.all()

      group_list = [group.to_dict() for group in groups]
      return group_list, "그룹 목록 조회 성공"
    except Exception as e:
        return None, f"그룹 목록 조회 중 오류가 발생했습니다: {str(e)}"


def update_company_group(db: Session, group_id: int, new_group_name: str):
    """
    CompanyGroup 레코드 업데이트

    Args:
        db (Session): 데이터베이스 세션
        group_id (int): 업데이트할 그룹 ID
        new_group_name (str): 새로운 그룹 이름

    Returns:
        tuple: (dict, str) - (업데이트된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        group = db.query(CompanyGroup).filter(CompanyGroup.group_id == group_id).first()
        if group:
          group.group_name = new_group_name
          db.commit()
          db.refresh(group)
          return group.to_dict(), "그룹이 성공적으로 수정되었습니다."
        return None, "해당하는 그룹이 없습니다."
    except IntegrityError:
      db.rollback()
      return None, "이미 존재하는 그룹 이름입니다."
    except Exception as e:
        db.rollback()
        return None, f"그룹 수정 중 오류가 발생했습니다: {str(e)}"


def delete_company_group(db: Session, group_id: int):
    """
    CompanyGroup 레코드 삭제

    Args:
        db (Session): 데이터베이스 세션
        group_id (int): 삭제할 그룹 ID

    Returns:
        tuple: (None, str) - (None, 메시지)
    """
    try:
        group = db.query(CompanyGroup).filter(CompanyGroup.group_id == group_id).first()
        if group:
          db.delete(group)
          db.commit()
          return None, "그룹이 성공적으로 삭제되었습니다."
        return None, "해당하는 그룹이 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"그룹 삭제 중 오류가 발생했습니다: {str(e)}"