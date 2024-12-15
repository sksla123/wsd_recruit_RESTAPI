from ..models.database import get_db
from ..models.user import create_user, get_user_by_id, update_user
from ..models.login import create_login, delete_login_by_refresh_token, get_login_by_refresh_token
from ..models.login_log import create_login_log
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
from ..utils.util import base64_encode, base64_decode, is_valid_email, now_korea

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
    
    user_id = data.get("user_id")
    refresh_token = data.get("refresh_token")

    if not (user_id and refresh_token):
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
        message = "사용자를 찾을 수 없습니다."
        return {"success": False, "message": message, "input_data": data}, message

    new_access_token = create_access_token(identity=user_id)

    message = "토큰 갱신 성공"
    return {
        "success": True,
        "message": message,
        "input_data": data,
        "access_token": new_access_token,
        "user": {"user_id": result["user"]["user_id"], "user_email": result["user"]["user_email"]}
    }, message

def update_user_profile(data):
    """
    프로필 업데이트 함수
    action: 
    1. 비밀번호 변경
    2. 이메일 정보 수정
    """
    db = get_db()
    user_id = data.get("user_id")
    action = data.get("action")
    
    if not (user_id and action):
        message = "필수 필드가 누락되었습니다."
        return {"success": False, "message": message, "input_data": data}, message

    if action == 1:  # 비밀번호 변경
        new_password = data.get("new_password")
        if not new_password:
            message = "새 비밀번호가 누락되었습니다."
            return {"success": False, "message": message, "input_data": data}, message
        encoded_password = base64_encode(new_password)
        result = update_user(db, user_id_input=user_id, new_user_password=encoded_password)
    elif action == 2:  # 이메일 정보 수정
        new_email = data.get("new_email")
        if not new_email:
            message = "새 이메일이 누락되었습니다."
            return {"success": False, "message": message, "input_data": data}, message
        result = update_user(db, user_id_input=user_id, new_user_email=new_email)
    else:
        message = "잘못된 action 값입니다."
        return {"success": False, "message": message, "input_data": data}, message

    message = "프로필 업데이트 성공" if result["success"] else "프로필 업데이트 실패"
    return {
        "success": result["success"],
        "message": message,
        "input_data": data,
        "user": result.get("user")
    }, message
