from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(255), unique=True, nullable=False)
    user_password = Column(String(255), nullable=False)
    user_authority = Column(String(50), default='user')
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    last_updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_date = Column(DateTime, nullable=True)

    logins = relationship('Login', back_populates='user')
    login_logs = relationship('LoginLog', back_populates='user')