from ..models.database import get_db
from ..models.user import create_user, get_user_by_id, update_user
from ..models.login import create_login, delete_login_by_refresh_token, get_login_by_refresh_token
from ..models.login_log import create_login_log
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
from ..utils.util import base64_encode, base64_decode, is_valid_email, now_korea, mysql_str_to_datetime

def register_user(data):
    """
    회원 가입 함수
    """
    _data = None
    db =  next(get_db())
    user_id = data.get("user_id")
    user_email = data.get("user_email")
    user_password = data.get("user_password")
    user_level = data.get("user_level")

    print('ello')
    if not is_valid_email(user_email):
        message = "적절한 이메일 형식이 아닙니다."
        return False, _data, message, 400

    if not (user_id and user_email and user_password and user_level):
        message = "필수 필드가 누락되었습니다."
        return False, _data, message, 400

    if user_level not in [5, 10]:
        message = "잘못된 user_level입니다. 5(company user) 또는 10(normal user)만 가능합니다."
        return False, _data, message, 400


    encoded_password = base64_encode(user_password)
    result = create_user(db, user_id=user_id, user_email=user_email, user_password=encoded_password, user_level=user_level)
    
    user_data = result.get("user")
    _data = {}

    if user_data is not None:
        _data = {
            "user_id" : user_data.get("user_id"),
            "user_email" : user_data.get("user_email"),
            "user_level" : user_data.get("user_level"),
            "created_date" : user_data.get("created_date")
            }

    message = "회원 가입 성공" if result["success"] else "회원 가입 실패"
    print(result.get('error', " "))

    if not result["success"] and 'pymysql.err.IntegrityError' in result.get('error', " "):
        message = "회원 가입 실패. 이미 가입한 회원입니다."
        return False, _data, message, 409

    return True, _data, "회원 가입에 성공하셨습니다.", 200

def user_login(data):
    """
    로그인 함수
    """
    _data = None
    db = next(get_db())
    
    user_id = data.get("user_id")
    user_password = data.get("user_password")

    if not (user_id and user_password):
        message = "필수 필드가 누락되었습니다."
        return False, _data, message, 400

    result = get_user_by_id(db, user_id)
    _data = {}

    if not result["success"]:
        message = "사용자를 찾을 수 없습니다."
        create_login_log(db, login_id=user_id, login_success=0)
        return False, _data, message, 400

    user = result["user"]

    if base64_decode(user["user_password"]) != user_password:
        message = "잘못된 비밀번호 입니다."
        create_login_log(db, login_id=user_id, login_success=0)
        return False, _data, _data, 400

    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    create_login_log(db, login_id=user_id, login_success=1)
    create_login(db, user_id=user_id, refresh_token=refresh_token, expires_at=now_korea() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'])

    message = "로그인 성공"
    _data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"user_id": user["user_id"], "user_email": user["user_email"]}
    }
    return True, _data, message, 200

def user_logout(data):
    """
    로그아웃 함수
    """
    _data = None
    db = next(get_db())
    
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        message = "필수 필드가 누락되었습니다."
        return False, _data, message, 400

    result = delete_login_by_refresh_token(db, refresh_token)
    _data = {}

    if not result["success"]:
        message = "로그인된 token이 없습니다."
        return False, _data, message, 400

    message = "Successfully logout"
    return True, _data, message, 200

def refresh_token(data):
    """
    토큰 갱신 함수
    """
    _data = None
    db = next(get_db())

    refresh_token = data.get("refresh_token")

    if not refresh_token:
        message = "refresh token이 누락되었습니다."
        return False, message, _data, 400

    _data = {}
    result = get_login_by_refresh_token(db, refresh_token)

    if not result["success"]:
        message = "로그인된 사용자를 찾을 수 없습니다."
        return False, message ,_data, 401

    login_data = result.get("login")
    # print(login_data)
    expire_date = mysql_str_to_datetime(login_data.get("expires_at"))

    if expire_date <= now_korea():
        # print(expire_date)
        # print(now_korea())
        message = "다시 로그인 해주세요."
        return False, message ,_data, 401

    user_id = login_data.get("user_id")
    new_access_token = create_access_token(identity=user_id)

    message = "토큰 갱신 성공"
    _data = {
        "user_id": user_id,
        "access_token": new_access_token,
    }
    return True, message, _data, 200

def update_user_profile(data):
    """
    프로필 업데이트 함수
    action: 
    1. 비밀번호 변경
    2. 이메일 정보 수정
    """
    _data = None
    db = next(get_db())
    
    user_id = data.get("user_id")
    action = data.get("action")
    new_value = data.get("new_value")

    if not (user_id and action and new_value):
        message = "필수 필드가 누락되었습니다."
        return False, _data, message, 400

    if action not in ["password", "email"]:
        message = "잘못된 action입니다. 'password' 또는 'email'만 가능합니다."
        return False, _data, message, 400

    result = get_user_by_id(db, user_id)
    if not result["success"]:
        message = "사용자를 찾을 수 없습니다."
        return False, _data, message, 404

    if action == "password":
        new_password = base64_encode(new_value)
        update_result = update_user(db, user_id, new_user_password=new_password)
    elif action == "email":
        if not is_valid_email(new_value):
            message = "적절한 이메일 형식이 아닙니다."
            return False, _data, message, 400
        update_result = update_user(db, user_id, new_user_email=new_value)

    if not update_result["success"]:
        message = f"{action} 업데이트에 실패했습니다."
        return False, _data, message, 500

    _data = {
        "user_id": user_id,
        "updated_field": action,
        "new_value": new_value if action == "email" else "******"
    }

    message = f"{action} 업데이트에 성공했습니다."
    return True, _data, message, 200
