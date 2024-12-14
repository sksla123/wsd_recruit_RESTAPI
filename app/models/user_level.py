# models/user_level.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class UserLevel(Base):
    """
    UserLevel 테이블 모델

    Attributes:
        user_level (int): 사용자 레벨 (PK)
        user_level_name (str): 사용자 레벨 명칭 (NN)
    """
    __tablename__ = 'UserLevel'

    user_level = Column(Integer, primary_key=True, comment="사용자 레벨")
    user_level_name = Column(String(255), nullable=False, comment="사용자 레벨 명칭")

    def to_dict(self):
        """
        모델 객체를 딕셔너리로 변환

        Returns:
            dict: 모델의 데이터를 담은 딕셔너리
        """
        return {
            "user_level": self.user_level,
            "user_level_name": self.user_level_name
        }

def create_user_level(db: Session, user_level: int, user_level_name: str):
    """
    새로운 UserLevel 레코드 생성

    Args:
        db (Session): 데이터베이스 세션
        user_level (int): 사용자 레벨
        user_level_name (str): 사용자 레벨 명칭

    Returns:
        tuple: (dict, str) - (생성된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        db_user_level = UserLevel(user_level=user_level, user_level_name=user_level_name)
        db.add(db_user_level)
        db.commit()
        db.refresh(db_user_level)
        return db_user_level.to_dict(), "사용자 레벨이 성공적으로 생성되었습니다."
    except IntegrityError:
        db.rollback()
        return None, "이미 존재하는 사용자 레벨입니다."
    except Exception as e:
        db.rollback()
        return None, f"사용자 레벨 생성 중 오류가 발생했습니다: {str(e)}"

def get_user_level(db: Session, user_level: int):
    """
    user_level로 UserLevel 레코드 조회

    Args:
        db (Session): 데이터베이스 세션
        user_level (int): 조회할 사용자 레벨

    Returns:
        tuple: (dict, str) - (조회된 데이터, 메시지) 또는 (None, 메시지)
    """
    try:
        user_level_obj = db.query(UserLevel).filter(UserLevel.user_level == user_level).first()
        if user_level_obj:
            return user_level_obj.to_dict(), "사용자 레벨 조회 성공"
        return None, "해당하는 사용자 레벨이 없습니다."
    except Exception as e:
        return None, f"사용자 레벨 조회 중 오류가 발생했습니다: {str(e)}"

def get_user_level_list(db: Session, page: int = 1, per_page: int = 20, pagination: bool = False):
    """
    UserLevel 레코드 목록 조회 (페이지네이션 지원)

    Args:
        db (Session): 데이터베이스 세션
        page (int): 페이지 번호 (기본값: 1)
        per_page (int): 페이지당 항목 수 (기본값: 20)
        pagination (bool): 페이지네이션 사용 여부 (기본값: False)

    Returns:
        tuple: (list, str) - (조회된 데이터 목록, 메시지) 또는 (None, 메시지)
    """
    try:
        query = db.query(UserLevel)
        if pagination:
            user_levels = query.offset((page - 1) * per_page).limit(per_page).all()
        else:
            user_levels = query.all()
        user_level_list = [user_level.to_dict() for user_level in user_levels]
        return user_level_list, "사용자 레벨 목록 조회 성공"
    except Exception as e:
        return None, f"사용자 레벨 목록 조회 중 오류가 발생했습니다: {str(e)}"

def update_user_level(db: Session, user_level: int, new_user_level_name: str):
    """
    UserLevel 레코드 업데이트

    Args:
        db (Session): 데이터베이스 세션
        user_level (int): 수정할 사용자 레벨
        new_user_level_name (str): 새로운 사용자 레벨 명칭

    Returns:
        tuple: (dict, str) - (업데이트된 데이터, 메시지) 또는 (None, 에러 메시지)
    """
    try:
        user_level_obj = db.query(UserLevel).filter(UserLevel.user_level == user_level).first()
        if user_level_obj:
            user_level_obj.user_level_name = new_user_level_name
            db.commit()
            db.refresh(user_level_obj)
            return user_level_obj.to_dict(), "사용자 레벨이 성공적으로 수정되었습니다."
        return None, "해당하는 사용자 레벨이 없습니다."
    except IntegrityError:
      db.rollback()
      return None, "이미 존재하는 사용자 레벨입니다." #이 부분은 PK라 의미 없음.
    except Exception as e:
        db.rollback()
        return None, f"사용자 레벨 수정 중 오류가 발생했습니다: {str(e)}"

def delete_user_level(db: Session, user_level: int):
    """
    UserLevel 레코드 삭제

    Args:
        db (Session): 데이터베이스 세션
        user_level (int): 삭제할 사용자 레벨

    Returns:
        tuple: (None, str) - (None, 메시지)
    """
    try:
        user_level_obj = db.query(UserLevel).filter(UserLevel.user_level == user_level).first()
        if user_level_obj:
            db.delete(user_level_obj)
            db.commit()
            return None, "사용자 레벨이 성공적으로 삭제되었습니다."
        return None, "해당하는 사용자 레벨이 없습니다."
    except Exception as e:
        db.rollback()
        return None, f"사용자 레벨 삭제 중 오류가 발생했습니다: {str(e)}"