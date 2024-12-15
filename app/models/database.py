# models/database.py

from . import Base, SQLALCHEMY_DATABASE_URI
# models/company_group.py 와 models/company.py의 각 CRUD 함수들이 정상적으로 동작하는지 테스트
# 각 함수의 반환 값을 모두 출력
# 각 모듈의 테스트가 끝날 때마다 총 n개 중 몇 개가 성공했고, 몇 개가 실패했는지 알림. (실패한 함수들이 누군지 따로 알리기)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session  # Session 임포트 추가

from .company_group import *
from .company import *

# 데이터베이스 엔진 생성 (echo=True로 쿼리 확인 가능)
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():  # Dependency Injection을 위한 함수
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from typing import List, Dict, Any

def run_test(db: Session, test_name: str, test_func, *args, **kwargs) -> Dict[str, Any]:
    """
    테스트 함수 실행 및 결과 반환.

    Args:
        db (Session): 데이터베이스 세션
        test_name (str): 테스트 이름
        test_func: 테스트 함수
        *args: 테스트 함수에 넘겨줄 가변 인자
        **kwargs: 테스트 함수에 넘겨줄 키워드 인자

    Returns:
        Dict[str, Any]: 테스트 결과 딕셔너리. {"success": True/False, "result": 테스트 결과, "error": 오류 메시지} 형태.
                        성공 시 {"success": True, "result": 테스트 결과}
                        실패 시 {"success": False, "error": 오류 메시지}
    """
    try:
        result = test_func(db, *args, **kwargs)
        print(f"{test_name}: {result}")  # 결과값 출력
        return {"success": True, "result": result}
    except Exception as e:
        print(f"{test_name} 실패: {e}") # 오류 출력
        return {"success": False, "error": str(e)}

def print_test_summary(test_name: str, test_results: List[Dict[str, Any]]): # 요약 출력 함수 분리
    """테스트 결과를 요약하여 출력합니다."""
    success_count = sum(1 for result in test_results if result["success"])
    fail_count = len(test_results) - success_count
    fail_details = [result["error"] for result in test_results if not result["success"]]

    print(f"\n{test_name} Test Summary:") # 함수 이름 인자로 받도록 수정
    print(f"  Successful tests: {success_count}")
    print(f"  Failed tests: {fail_count}")
    if fail_details:
        print("  Failed tests details:")
        for detail in fail_details:
            print(f"    - {detail}")

def test_company_and_group_models(db: Session):
    """CompanyGroup과 Company의 CRUD 함수들을 테스트합니다."""
    test_results: List[Dict[str, Any]] = [] # 테스트 결과를 저장할 리스트

    print("\nTesting CompanyGroup functions:")
    test_results.append(run_test(db, "get_company_groups", get_company_groups))
    test_results.append(run_test(db, "create_company_group", create_company_group, "Test Group"))

    test_group = db.query(CompanyGroup).filter(CompanyGroup.group_name == "Test Group").first()
    group_id_for_test = test_group.group_id if test_group else None
    test_results.append(run_test(db, "get_company_group_by_id", get_company_group_by_id, group_id_for_test))
    test_results.append(run_test(db, "update_company_group", update_company_group, group_id_for_test, "Updated Test Group"))
    test_results.append(run_test(db, "delete_company_group", delete_company_group, group_id_for_test))

    print("\nTesting Company functions:")
    test_results.append(run_test(db, "get_companies", get_companies))
    test_results.append(run_test(db, "create_company", create_company, "Test Company", "http://test.com", group_id_for_test))

    test_company = db.query(Company).filter(Company.comp_name == "Test Company").first()
    comp_id_for_test = test_company.comp_id if test_company else None

    test_results.append(run_test(db, "get_company_by_id", get_company_by_id, comp_id_for_test))
    test_results.append(run_test(db, "update_company", update_company, comp_id_for_test, "Updated Test Company"))
    test_results.append(run_test(db, "delete_company", delete_company, comp_id_for_test))

    print_test_summary("Company and Group Models", test_results)

    # 테스트 후 데이터베이스 정리 (테스트 데이터 삭제)
    try:
        db.query(Company).filter(Company.comp_name.like("Test%")).delete(synchronize_session=False)
        db.query(CompanyGroup).filter(CompanyGroup.group_name.like("Test%")).delete(synchronize_session=False)
        db.commit()
        print("테스트 데이터 삭제 완료")
    except Exception as e:
        db.rollback()
        print(f"테스트 데이터 삭제 실패: {e}")

from .edu_code import *
def test_edu_code_model(db: Session):
    test_results: List[Dict[str, Any]] = []

    print("\nTesting EduCode functions:")
    test_results.append(run_test(db, "get_edu_codes", get_edu_codes))
    test_results.append(run_test(db, "create_edu_code", create_edu_code, 100, "테스트 학력"))
    test_results.append(run_test(db, "get_edu_code_by_id", get_edu_code_by_id, 100))  # Existing edu_code
    test_results.append(run_test(db, "get_edu_code_by_id", get_edu_code_by_id, 9999))  # Non-existent edu_code

    # Test update with existing and non-existent edu_code
    test_results.append(run_test(db, "update_edu_code", update_edu_code, 100, "업데이트된 학력"))
    test_results.append(run_test(db, "update_edu_code", update_edu_code, 9999, "업데이트 실패 (존재하지 않음)"))

    test_results.append(run_test(db, "delete_edu_code", delete_edu_code, 100))

    # Test delete with non-existent edu_code (should still be successful)
    test_results.append(run_test(db, "delete_edu_code", delete_edu_code, 9999))

    print_test_summary("EduCode Model", test_results) # 요약 출력 함수 호출

from .job_code import *
def test_job_code_model(db: Session): # JobCode 테스트 함수 추가
    test_results: List[Dict[str, Any]] = []

    print("\nTesting JobCode functions:")
    test_results.append(run_test(db, "get_job_codes", get_job_codes))
    test_results.append(run_test(db, "create_job_code", create_job_code, 200, "테스트 직업"))
    test_results.append(run_test(db, "get_job_code_by_id", get_job_code_by_id, 200))
    test_results.append(run_test(db, "get_job_code_by_id", get_job_code_by_id, 8888)) # Non-existent ID 테스트

    test_results.append(run_test(db, "update_job_code", update_job_code, 200, "업데이트된 직업"))
    test_results.append(run_test(db, "update_job_code", update_job_code, 8888, "업데이트 실패 (존재하지 않음)"))

    test_results.append(run_test(db, "delete_job_code", delete_job_code, 200))
    test_results.append(run_test(db, "delete_job_code", delete_job_code, 8888)) # Non-existent ID 삭제 시도

    print_test_summary("JobCode Model", test_results)

from .job_posting_job import *
def test_job_posting_job_model(db: Session):
    """JobPostingJob 모델에 대한 CRUD 함수들을 테스트합니다."""
    test_results: List[Dict[str, Any]] = []

    print("\nTesting JobPostingJob functions:")

    # Assuming you have existing job_posting and job_code data (adjust based on your setup)
    test_poster_id = "poster123"
    test_job_code = 101

    test_results.append(run_test(db, "get_job_posting_jobs", get_job_posting_jobs))
    test_results.append(run_test(db, "create_job_posting_job", create_job_posting_job, test_poster_id, test_job_code))
    test_results.append(run_test(db, "get_job_posting_job_by_ids", get_job_posting_job_by_ids, test_poster_id, test_job_code))

    # Test with non-existent poster_id or job_code
    test_results.append(run_test(db, "get_job_posting_job_by_ids", get_job_posting_job_by_ids, "non-existent-poster", test_job_code))
    test_results.append(run_test(db, "get_job_posting_job_by_ids", get_job_posting_job_by_ids, test_poster_id, 9999))

    test_results.append(run_test(db, "delete_job_posting_job", delete_job_posting_job, test_poster_id, test_job_code))

    # Test delete with non-existent poster_id or job_code (should still be successful)
    test_results.append(run_test(db, "delete_job_posting_job", delete_job_posting_job, "non-existent-poster", test_job_code))
    test_results.append(run_test(db, "delete_job_posting_job", delete_job_posting_job, test_poster_id, 9999))

    # ... (Add more test cases as needed)

    print_test_summary("JobPostingJob Model", test_results)

from .job_posting_loc import *
def test_job_posting_loc_model(db: Session):
    """JobPostingLoc 모델에 대한 CRUD 함수들을 테스트합니다."""
    test_results: List[Dict[str, Any]] = []

    print("\nTesting JobPostingLoc functions:")

    # Assuming you have existing job_posting and loc_code data (adjust based on your setup)
    test_poster_id = "poster123"
    test_loc_code = 202

    test_results.append(run_test(db, "get_job_posting_locs", get_job_posting_locs))
    test_results.append(run_test(db, "create_job_posting_loc", create_job_posting_loc, test_poster_id, test_loc_code))
    test_results.append(run_test(db, "get_job_posting_loc_by_ids", get_job_posting_loc_by_ids, test_poster_id, test_loc_code))

    # Test with non-existent poster_id or loc_code
    test_results.append(run_test(db, "get_job_posting_loc_by_ids", get_job_posting_loc_by_ids, "non-existent-poster", test_loc_code))
    test_results.append(run_test(db, "get_job_posting_loc_by_ids", get_job_posting_loc_by_ids, test_poster_id, 9999))

    test_results.append(run_test(db, "delete_job_posting_loc", delete_job_posting_loc, test_poster_id, test_loc_code))

    # Test delete with non-existent poster_id or loc_code (should still be successful)
    test_results.append(run_test(db, "delete_job_posting_loc", delete_job_posting_loc, "non-existent-poster", test_loc_code))
    test_results.append(run_test(db, "delete_job_posting_loc", delete_job_posting_loc, test_poster_id, 9999))

    # ... (Add more test cases as needed)

    print_test_summary("JobPostingLoc Model", test_results)

from .job_posting import *
def test_job_posting_model(db: Session):
    """JobPosting 모델에 대한 CRUD 함수들을 테스트합니다."""
    test_results: List[Dict[str, Any]] = []

    print("\nTesting JobPosting functions:")

    # 테스트 데이터 (딕셔너리로 관리)
    test_data = {
        "comp_id": 101,
        "poster_id": "poster123",
        "poster_title": "Software Engineer Intern",
        "edu_code": 2,
        "sal_code": 3,
        "poster_writer_user_id": "user1"
    }

    # get_job_postings 테스트
    test_results.append(run_test(db, "get_job_postings 테스트", get_job_postings))

    # 정렬 테스트
    test_results.append(run_test(db, "get_job_postings_sorted_by 테스트 (마감일 순)", get_job_postings_sorted_by, sort_criteria={"deadline_date": 1}, page=1, item_counts=20))
    test_results.append(run_test(db, "get_job_postings_sorted_by 테스트 (제목 순)", get_job_postings_sorted_by, sort_criteria={"poster_title": 0}, page=1, item_counts=20))

    # get_available_job_postings_sorted_by 테스트
    test_results.append(run_test(db, "get_available_job_postings_sorted_by 테스트", get_available_job_postings_sorted_by, sort_criteria={"deadline_date": 0}, page=1, item_counts=20))

    # create_job_posting 테스트 (필수 필드만 사용)
    test_results.append(run_test(db, "create_job_posting 테스트 (필수 필드만)", create_job_posting,
                                test_data["comp_id"], test_data["poster_id"], test_data["poster_title"],
                                edu_code=test_data["edu_code"], sal_code=test_data["sal_code"],
                                poster_writer_user_id=test_data["poster_writer_user_id"]))

    # create_job_posting 테스트 (선택적 필드 포함)
    test_results.append(run_test(db, "create_job_posting 테스트 (선택적 필드 포함)", create_job_posting,
                                test_data["comp_id"], test_data["poster_id"] + "2", test_data["poster_title"],
                                job_sectors="Backend Development", deadline_date=date.today(),
                                edu_code=test_data["edu_code"], sal_code=test_data["sal_code"],
                                poster_writer_user_id=test_data["poster_writer_user_id"]))

    # 필수 필드 누락 시 create_job_posting 테스트 (오류 발생 테스트)
    test_results.append(run_test(db, "create_job_posting 테스트 (poster_title 누락 - 실패)", create_job_posting, test_data["comp_id"], test_data["poster_id"] + "3"))

    # get_job_posting_by_id 테스트
    test_results.append(run_test(db, "get_job_posting_by_id 테스트 (존재하는 ID)", get_job_posting_by_id, test_data["poster_id"]))
    test_results.append(run_test(db, "get_job_posting_by_id 테스트 (존재하지 않는 ID)", get_job_posting_by_id, "non-existent-id"))

    # update_job_posting 테스트
    test_results.append(run_test(db, "update_job_posting 테스트", update_job_posting, test_data["poster_id"], new_poster_title="Software Engineer"))
    test_results.append(run_test(db, "update_job_posting 테스트 (마감일 변경)", update_job_posting, test_data["poster_id"] + "2", new_deadline_date=date.today()))
    test_results.append(run_test(db, "update_job_posting 테스트 (존재하지 않는 ID 업데이트 시도 - 실패)", update_job_posting, "non-existent-id", new_poster_title="This should fail"))

    # delete_job_posting 테스트
    test_results.append(run_test(db, "delete_job_posting 테스트", delete_job_posting, test_data["poster_id"]))
    test_results.append(run_test(db, "delete_job_posting 테스트 (존재하지 않는 ID 삭제 시도)", delete_job_posting, "non-existent-id"))

    print_test_summary("JobPosting Model", test_results)

from .loc_code import *
def test_loc_codes_model(db: Session):
    """LocCode 모델에 대한 CRUD 함수들을 테스트합니다."""
    test_results: List[Dict[str, Any]] = []

    print("\nTesting LocCode functions:")

    # 테스트 데이터 설정
    test_loc_data = {
        "loc_code": 999,  # 테스트에 사용할 새로운 loc_code
        "loc_name": "Test Location",
        "loc_mcode": 888,
        "loc_mname": "Test Main Location",
        "updated_loc_name": "Updated Test Location",
        "updated_loc_mcode": 777,
        "updated_loc_mname": "Updated Main Location"
    }
    non_existent_loc_code = 123456789  # 존재하지 않는 loc_code

    # get_loc_codes 테스트
    test_results.append(run_test(db, "get_loc_codes 테스트", get_loc_codes))

    # create_loc_code 테스트 (성공)
    test_results.append(run_test(db, "create_loc_code 테스트 (성공)", create_loc_code,
                                test_loc_data["loc_code"], test_loc_data["loc_name"],
                                test_loc_data["loc_mcode"], test_loc_data["loc_mname"]))

    # create_loc_code 테스트 (중복 코드 생성 - 실패)
    test_results.append(run_test(db, "create_loc_code 테스트 (중복 코드 - 실패)", create_loc_code,
                                test_loc_data["loc_code"], "Another Name"))

    # get_loc_code_by_id 테스트 (존재하는 ID)
    test_results.append(run_test(db, "get_loc_code_by_id 테스트 (존재)", get_loc_code_by_id, test_loc_data["loc_code"]))

    # get_loc_code_by_id 테스트 (존재하지 않는 ID)
    test_results.append(run_test(db, "get_loc_code_by_id 테스트 (미존재)", get_loc_code_by_id, non_existent_loc_code))

    # update_loc_code 테스트 (성공)
    test_results.append(run_test(db, "update_loc_code 테스트 (성공)", update_loc_code,
                                test_loc_data["loc_code"], test_loc_data["updated_loc_name"],
                                test_loc_data["updated_loc_mcode"], test_loc_data["updated_loc_mname"]))

    # update_loc_code 테스트 (존재하지 않는 ID - 실패)
    test_results.append(run_test(db, "update_loc_code 테스트 (미존재 ID - 실패)", update_loc_code, non_existent_loc_code, "Should Fail"))

    # delete_loc_code 테스트 (성공)
    test_results.append(run_test(db, "delete_loc_code 테스트 (성공)", delete_loc_code, test_loc_data["loc_code"]))

    # delete_loc_code 테스트 (이미 삭제된 ID - 실패)
    test_results.append(run_test(db, "delete_loc_code 테스트 (이미 삭제된 ID - 실패)", delete_loc_code, test_loc_data["loc_code"]))

    print_test_summary("LocCode Model", test_results)

from .user import *
def test_user_model(db: Session):
    """User 모델에 대한 CRUD 함수들을 테스트합니다."""
    test_results: List[Dict[str, Any]] = []

    print("\nTesting User functions:")

    # 테스트 데이터 (딕셔너리로 관리)
    test_user_data = {
        "user_id": "test_user",
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User",
        "is_admin": False,
        "updated_name": "Updated Test User",
        "updated_email": "updated@example.com"
    }
    non_existent_user_id = "non_existent_user"

    # get_users 테스트
    test_results.append(run_test(db, "get_users 테스트", get_users))

    # create_user 테스트 (성공)
    test_results.append(run_test(db, "create_user 테스트 (성공)", create_user,
                                 test_user_data["user_id"],
                                 test_user_data["email"],
                                 test_user_data["password"],
                                 test_user_data["name"]))

    # create_user 테스트 (중복 user_id - 실패)
    test_results.append(run_test(db, "create_user 테스트 (중복 user_id - 실패)", create_user,
                                 test_user_data["user_id"], # 동일 user_id 사용
                                 "another@example.com", # 다른 이메일
                                 "Another Name",
                                 ))

    # create_user 테스트 (중복 email - 실패)
    test_results.append(run_test(db, "create_user 테스트 (중복 email - 실패)", create_user,
                                 "another_user_id", # 다른 user_id
                                 test_user_data["email"], # 동일 이메일 사용
                                 "Another Name",
                                ))

    # get_user_by_id 테스트 (존재하는 유저)
    test_results.append(run_test(db, "get_user_by_id 테스트 (존재)", get_user_by_id, test_user_data["user_id"]))

    # get_user_by_id 테스트 (존재하지 않는 유저)
    test_results.append(run_test(db, "get_user_by_id 테스트 (미존재)", get_user_by_id, non_existent_user_id))

    # update_user 테스트 (성공)
    test_results.append(run_test(db, "update_user 테스트 (성공)", update_user,
                                 test_user_data["user_id"],
                                 new_name=test_user_data["updated_name"],
                                 new_email=test_user_data["updated_email"]))

    # update_user 테스트 (존재하지 않는 user_id - 실패)
    test_results.append(run_test(db, "update_user 테스트 (미존재 user_id - 실패)", update_user,
                                 non_existent_user_id, new_name="Should Fail"))

    # delete_user 테스트 (성공)
    test_results.append(run_test(db, "delete_user 테스트 (성공)", delete_user, test_user_data["user_id"]))

    # delete_user 테스트 (이미 삭제된 user_id - 실패)
    test_results.append(run_test(db, "delete_user 테스트 (이미 삭제된 user_id - 실패)", delete_user, test_user_data["user_id"]))
    
    print_test_summary("User Model", test_results)

from .login_log import *
def test_login_log_model(db: Session):
  """LoginLog 모델의 CRUD 함수들을 테스트합니다."""
  test_results: List[Dict[str, Any]] = []  # 테스트 결과 저장 리스트

  print("\nTesting LoginLog functions:")

  # 샘플 로그 생성
  test_results.append(run_test(db, "create_login_log", create_login_log, login_id="admin", login_success=1))
  test_results.append(run_test(db, "create_login_log", create_login_log, login_id="user1", login_success=1))
  test_results.append(run_test(db, "create_login_log", create_login_log, login_id="user2", login_success=0))
  db.commit()

  # 전체 로그 목록 조회 테스트
  test_results.append(run_test(db, "get_login_logs", get_login_logs))

  # 특정 로그 ID로 조회 테스트
  created_log = db.query(LoginLog).filter(LoginLog.login_id == "user1").first()
  if created_log:
      test_results.append(run_test(db, "get_login_log_by_id", get_login_log_by_id, 0))
  else:
      print("테스트 로그 생성 실패")

  # 로그 생성 테스트
  test_results.append(run_test(db, "create_login_log", create_login_log, login_id="user3", login_ip="127.0.0.1"))

  # 로그 삭제 테스트 (만약 위 테스트에서 생성된 로그가 있다면)
  if created_log:
      test_results.append(run_test(db, "delete_login_log", delete_login_log, created_log.login_log_id))

  # 특정 사용자 ID의 로그 목록 조회 테스트
  test_results.append(run_test(db, "get_login_logs_by_login_id", get_login_logs_by_login_id, login_id_input="admin"))

  print_test_summary("LoginLog Model", test_results)

  # 테스트 데이터 정리
  try:
      db.query(LoginLog).filter(LoginLog.login_id.in_(["user1", "user2", "user3"])).delete(synchronize_session=False)
      db.commit()
      print("테스트 데이터 삭제 완료")
  except Exception as e:
      db.rollback()
      print(f"테스트 데이터 삭제 실패: {e}")

from .login import *
from datetime import datetime, timedelta
def test_login_model(db: Session):
    """Login 모델의 CRUD 함수들을 테스트합니다."""
    test_results = []

    print("\nTesting Login functions:")

    # Create Test
    test_results.append(run_test(db, "create_login", create_login, user_id="testuser1", refresh_token="token1", expires_at=datetime.utcnow() + timedelta(days=1)))
    test_results.append(run_test(db, "create_login", create_login, user_id="testuser2", refresh_token="token2", expires_at=datetime.utcnow() + timedelta(days=2), login_ip="127.0.0.1"))
    db.commit()

    # Read (get_logins) Test
    test_results.append(run_test(db, "get_logins", get_logins))

    # Read (get_login_by_refresh_id) Test
    created_login = db.query(Login).filter(Login.user_id == "testuser1").first()
    refresh_id_for_test = created_login.refresh_id if created_login else None
    test_results.append(run_test(db, "get_login_by_refresh_id", get_login_by_refresh_id, refresh_id_for_test))

    # Read (get_login_by_user_id) Test
    test_results.append(run_test(db, "get_login_by_user_id", get_login_by_user_id, "testuser2"))

    # Delete Test
    if refresh_id_for_test:
        test_results.append(run_test(db, "delete_login", delete_login, refresh_id_for_test))

    print_test_summary("Login Model", test_results)

    # Cleanup Test Data
    try:
        db.query(Login).filter(Login.user_id.in_(["testuser1", "testuser2"])).delete(synchronize_session=False)
        db.commit()
        print("테스트 데이터 삭제 완료")
    except Exception as e:
        db.rollback()
        print(f"테스트 데이터 삭제 실패: {e}")

from .sal_code import *

def test_sal_code_model(db: Session):
    """SalCode 모델의 CRUD 함수들을 테스트합니다."""
    test_results = []

    print("\nTesting SalCode functions:")

    # Create Test
    test_results.append(run_test(db, "create_sal_code", create_sal_code, sal_code=100, sal_name="test_code1"))
    test_results.append(run_test(db, "create_sal_code", create_sal_code, sal_code=200, sal_name="test_code2"))
    db.commit()

    # Read (get_sal_codes) Test
    test_results.append(run_test(db, "get_sal_codes", get_sal_codes))

    # Read (get_sal_code_by_id) Test
    created_sal_code = db.query(SalCode).filter(SalCode.sal_code == 100).first()
    sal_code_id_for_test = created_sal_code.sal_code if created_sal_code else None
    test_results.append(run_test(db, "get_sal_code_by_id", get_sal_code_by_id, sal_code_id_for_test))

    # Update Test
    if sal_code_id_for_test:
        test_results.append(run_test(db, "update_sal_code", update_sal_code, sal_code_id_for_test, new_sal_name="updated_code"))

    # Read (get_sal_code_by_id) Test (후 수정 확인)
    test_results.append(run_test(db, "get_sal_code_by_id", get_sal_code_by_id, sal_code_id_for_test))

    # Delete Test
    if sal_code_id_for_test:
        test_results.append(run_test(db, "delete_sal_code", delete_sal_code, sal_code_id_for_test))

    print_test_summary("SalCode Model", test_results)

    # Cleanup Test Data
    try:
        db.query(SalCode).filter(SalCode.sal_code.in_([100, 200])).delete(synchronize_session=False)
        db.commit()
        print("테스트 데이터 삭제 완료")
    except Exception as e:
        db.rollback()
        print(f"테스트 데이터 삭제 실패: {e}")

from .user_applicated_log import *
from enum import Enum
def test_user_applicated_log_model(db: Session):
    """UserApplicatedLog 모델의 CRUD 함수들을 테스트합니다."""
    test_results = []

    print("\nTesting UserApplicatedLog functions:")

    # Create Test
    test_results.append(run_test(db, "create_user_applicated_log", create_user_applicated_log, application_id=1, user_id="testuser1", poster_id="poster1", applicate_action=ApplicateAction.CREATE))
    test_results.append(run_test(db, "create_user_applicated_log", create_user_applicated_log, application_id=2, user_id="testuser2", poster_id="poster2", applicate_action=ApplicateAction.UPDATE))
    db.commit()

    # Read (get_user_applicated_logs) Test
    test_results.append(run_test(db, "get_user_applicated_logs", get_user_applicated_logs))

    # Read (get_user_applicated_log_by_id) Test
    created_log = db.query(UserApplicatedLog).filter(UserApplicatedLog.application_id == 1).first()
    application_log_id_for_test = created_log.application_log_id if created_log else None
    test_results.append(run_test(db, "get_user_applicated_log_by_id", get_user_applicated_log_by_id, application_log_id_for_test))

    # Read (get_user_applicated_logs_by_app_id) Test
    test_results.append(run_test(db, "get_user_applicated_logs_by_app_id", get_user_applicated_logs_by_app_id, application_id_input=1))

    # Delete Test
    if application_log_id_for_test:
        test_results.append(run_test(db, "delete_user_applicated_log", delete_user_applicated_log, application_log_id_for_test))

    print_test_summary("UserApplicatedLog Model", test_results)

    # Cleanup Test Data
    try:
        db.query(UserApplicatedLog).filter(UserApplicatedLog.application_id.in_([1, 2])).delete(synchronize_session=False)
        db.commit()
        print("테스트 데이터 삭제 완료")
    except Exception as e:
        db.rollback()
        print(f"테스트 데이터 삭제 실패: {e}")

from .user_applicated import *
def test_user_applicated_model(db: Session):
    """UserApplicated 모델의 CRUD 함수들을 테스트합니다."""
    test_results = []

    print("\nTesting UserApplicated functions:")

    # Create Test
    test_results.append(run_test(db, "create_user_applicated", create_user_applicated, user_id="testuser1", poster_id="poster1", application="This is a test application", application_status=ApplicationStatus.APPLIED))
    test_results.append(run_test(db, "create_user_applicated", create_user_applicated, user_id="testuser2", poster_id="poster2", application="Another test application", application_status=ApplicationStatus.CANCELLED))
    db.commit()

    # Read (get_user_applicateds) Test
    test_results.append(run_test(db, "get_user_applicateds", get_user_applicateds))

    # Read (get_user_applicated_by_id) Test
    created_applicated = db.query(UserApplicated).filter(UserApplicated.user_id == "testuser1").first()
    application_id_for_test = created_applicated.application_id if created_applicated else None
    test_results.append(run_test(db, "get_user_applicated_by_id", get_user_applicated_by_id, application_id_for_test))

    # Update Test
    if application_id_for_test:
        test_results.append(run_test(db, "update_user_applicated", update_user_applicated, application_id_for_test, new_application="Updated application content", new_application_status=ApplicationStatus.ACCEPTED))

    # Read (get_user_applicated_by_id) Test (후 수정 확인)
    test_results.append(run_test(db, "get_user_applicated_by_id", get_user_applicated_by_id, application_id_for_test))

    # Delete Test
    if application_id_for_test:
        test_results.append(run_test(db, "delete_user_applicated", delete_user_applicated, application_id_for_test))

    print_test_summary("UserApplicated Model", test_results)

    # Cleanup Test Data
    try:
        db.query(UserApplicated).filter(UserApplicated.user_id.in_(["testuser1", "testuser2"])).delete(synchronize_session=False)
        db.commit()
        print("테스트 데이터 삭제 완료")
    except Exception as e:
        db.rollback()
        print(f"테스트 데이터 삭제 실패: {e}")

from .user_bookmark import *
def test_user_bookmark_model(db: Session):
    """UserBookmark 모델의 CRUD 함수들을 테스트합니다."""
    test_results = []

    print("\nTesting UserBookmark functions:")

    # Create Test
    test_results.append(run_test(db, "create_user_bookmark", create_user_bookmark, user_id="testuser1", poster_id="poster1"))
    test_results.append(run_test(db, "create_user_bookmark", create_user_bookmark, user_id="testuser2", poster_id="poster2"))
    db.commit()

    # Read (get_user_bookmarks) Test
    test_results.append(run_test(db, "get_user_bookmarks", get_user_bookmarks))

    # Read (get_user_bookmark_by_ids) Test
    test_results.append(run_test(db, "get_user_bookmark_by_ids", get_user_bookmark_by_ids, user_id_input="testuser1", poster_id_input="poster1"))

    # Delete Test
    test_results.append(run_test(db, "delete_user_bookmark", delete_user_bookmark, user_id_input="testuser1", poster_id_input="poster1"))

    print_test_summary("UserBookmark Model", test_results)

    # Cleanup Test Data
    try:
        db.query(UserBookmark).filter(UserBookmark.user_id.in_(["testuser1", "testuser2"])).delete(synchronize_session=False)
        db.commit()
        print("테스트 데이터 삭제 완료")
    except Exception as e:
        db.rollback()
        print(f"테스트 데이터 삭제 실패: {e}")

from .user_level import *
def test_user_level_model(db: Session):
    """UserLevel 모델의 CRUD 함수들을 테스트합니다."""
    test_results = []

    print("\nTesting UserLevel functions:")

    # Create Test
    test_results.append(run_test(db, "create_user_level", create_user_level, level=1, level_name="Beginner"))
    test_results.append(run_test(db, "create_user_level", create_user_level, level=2, level_name="Intermediate"))
    db.commit()

    # Read (get_user_levels) Test
    test_results.append(run_test(db, "get_user_levels", get_user_levels))

    # Read (get_user_level_by_id) Test
    created_level = db.query(UserLevel).filter(UserLevel.user_level == 1).first()
    level_id_for_test = created_level.user_level if created_level else None
    test_results.append(run_test(db, "get_user_level_by_id", get_user_level_by_id, level_id_for_test))

    # Update Test
    if level_id_for_test:
        test_results.append(run_test(db, "update_user_level", update_user_level, level_id_for_test, new_level_name="Advanced Beginner"))

    # Read (get_user_level_by_id) Test (후 수정 확인)
    test_results.append(run_test(db, "get_user_level_by_id", get_user_level_by_id, level_id_for_test))

    # Delete Test
    if level_id_for_test:
        test_results.append(run_test(db, "delete_user_level", delete_user_level, level_id_for_test))

    print_test_summary("UserLevel Model", test_results)

    # Cleanup Test Data
    try:
        db.query(UserLevel).filter(UserLevel.user_level.in_([1, 2])).delete(synchronize_session=False)
        db.commit()
        print("테스트 데이터 삭제 완료")
    except Exception as e:
        db.rollback()
        print(f"테스트 데이터 삭제 실패: {e}")

db = SessionLocal()
# db = get_db()

if __name__ == "__main__":
    try:
        test_company_and_group_models(db)
        test_edu_code_model(db)
        test_job_code_model(db)
        test_job_posting_job_model(db)
        test_job_posting_loc_model(db)
        test_job_posting_model(db)
        test_loc_codes_model(db)
        test_user_model(db)
        test_login_log_model(db)
        test_login_model(db)
        test_sal_code_model(db)
        test_user_applicated_log_model(db)
        test_user_applicated_model(db)
        test_user_bookmark_model(db)
        test_user_level_model(db)
    finally:
        db.close()