from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

class AuthService:
    @staticmethod
    def register_user(email, password):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")
        
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, user_authority='user')
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

    @staticmethod
    def update_user_profile(user_id, data):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return user