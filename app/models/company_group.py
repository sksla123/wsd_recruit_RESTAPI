# models/company_group.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Session
from .database import Base

from sqlalchemy import create_engine

class CompanyGroup(Base):
    """
    CompanyGroup 테이블에 대한 SQLAlchemy 모델 클래스
    """
    __tablename__ = "CompanyGroup"

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255))

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
    

if __name__ == "__main__":
    from .database import engine, SessionLocal
    from dotenv import load_dotenv

    load_dotenv()

    Base.metadata.create_all(engine)
    db = SessionLocal()

    test_results = []  # 테스트 결과를 저장할 리스트

    try:
        # 테스트 로직
        print("--- CREATE TEST ---")
        create_result = create_company_group(db, "Test Group 1")
        print(create_result)
        test_results.append(create_result["success"])

        print("--- GET ALL TEST ---")
        get_all_result = get_company_groups(db)
        print(get_all_result)
        test_results.append(get_all_result.get("success", True))

        if create_result["success"]:
            created_group_id = create_result["group"]["group_id"]

            print("--- GET BY ID TEST ---")
            get_by_id_result = get_company_group_by_id(db, created_group_id)
            print(get_by_id_result)
            test_results.append(get_by_id_result["success"])

            print("--- UPDATE TEST ---")
            update_result = update_company_group(db, created_group_id, "Updated Test Group")
            print(update_result)
            test_results.append(update_result["success"])

            print("--- DELETE TEST ---")
            delete_result = delete_company_group(db, created_group_id)
            print(delete_result)
            test_results.append(delete_result["success"])

            print("--- GET ALL TEST(after DELETE) ---")
            get_all_result_after_delete = get_company_groups(db)
            print(get_all_result_after_delete)
            test_results.append(get_all_result_after_delete.get("success", True))

        else:
            print("그룹 생성 실패로 나머지 테스트 생략")

    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
        test_results.append(False)  # 오류 발생 시 테스트 실패로 처리
    finally:
        db.close()

    # 최종 테스트 결과 출력
    all_tests_passed = all(test_results)  # 모든 요소가 True인지 확인
    if all_tests_passed:
        print("\n 모든 테스트를 통과했습니다!")
    else:
        print("\n 테스트 중 실패한 부분이 있습니다.")
        for i, result in enumerate(test_results):
            if not result:
                print(f" {i+1}번째 테스트 실패")