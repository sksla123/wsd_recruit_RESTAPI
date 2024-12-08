import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import current_app
from app.models.user import User
from app.models.login import Login
from app.models.login_log import LoginLog
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def register_user(self, email, password):
        # 사용자 등록 로직
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        new_user = User(
            user_email=email,
            user_password=hashed_password.decode('utf-8')
        )
        self.db.add(new_user)
        self.db.commit()
        return new_user

    def login_user(self, email, password, ip_address, device_info):
        # 로그인 로직
        user = self.db.query(User).filter_by(user_email=email).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.user_password.encode('utf-8')):
            # JWT 토큰 생성
            access_token = self.generate_access_token(user)
            refresh_token = self.generate_refresh_token(user)
            
            # 로그인 로그 생성
            login_log = LoginLog(
                login_ip=ip_address,
                device_info=device_info,
                status='success'
            )
            self.db.add(login_log)
            
            # 리프레시 토큰 저장
            login_record = Login(
                refresh_token=refresh_token,
                user_id=user.user_id,
                device_info=device_info,
                expired_date=datetime.utcnow() + current_app.config['REFRESH_TOKEN_DURATION']
            )
            self.db.add(login_record)
            
            self.db.commit()
            
            return access_token, refresh_token
        
        # 로그인 실패 로그
        login_log = LoginLog(
            login_ip=ip_address,
            device_info=device_info,
            status='failed'
        )
        self.db.add(login_log)
        self.db.commit()
        
        return None, None

    def generate_access_token(self, user):
        payload = {
            'user_id': user.user_id,
            'email': user.user_email,
            'exp': datetime.utcnow() + current_app.config['ACCESS_TOKEN_DURATION']
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    def generate_refresh_token(self, user):
        payload = {
            'user_id': user.user_id,
            'exp': datetime.utcnow() + current_app.config['REFRESH_TOKEN_DURATION']
        }
        return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')