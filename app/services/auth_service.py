import bcrypt
from app.models.user import User
from app.models.login import Login, LoginLog
from app import db
from app.utils.token_manager import TokenManager
from sqlalchemy.exc import IntegrityError

class AuthService:
    def register(self, email, password):
        # 비밀번호 해싱
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            new_user = User(
                user_email=email,
                user_password=hashed_password.decode('utf-8')
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            return None

    def login(self, email, password, ip_address, device_info):
        user = User.query.filter_by(user_email=email).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.user_password.encode('utf-8')):
            # 액세스 및 리프레시 토큰 생성
            access_token = TokenManager.generate_access_token(user.user_id)
            refresh_token = TokenManager.generate_refresh_token(user.user_id)
            
            # 로그인 기록
            login_record = Login(
                refresh_token=refresh_token,
                user_id=user.user_id,
                device_info=device_info
            )
            
            login_log = LoginLog(
                user_id=user.user_id,
                login_ip=ip_address,
                device_info=device_info,
                status='success'
            )
            
            db.session.add(login_record)
            db.session.add(login_log)
            db.session.commit()
            
            return access_token, refresh_token
        
        # 로그인 실패 기록
        failed_log = LoginLog(
            user_id=user.user_id if user else None,
            login_ip=ip_address,
            device_info=device_info,
            status='failed'
        )
        db.session.add(failed_log)
        db.session.commit()
        
        return None, None