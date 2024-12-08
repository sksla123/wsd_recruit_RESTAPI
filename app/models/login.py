from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime, timedelta

class Login(db.Model):
    __tablename__ = 'logins'
    
    refresh_token = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    device_info = Column(String(255))
    created_date = Column(DateTime, default=datetime.utcnow)
    expired_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))

    user = relationship('User', back_populates='logins')

class LoginLog(db.Model):
    __tablename__ = 'login_logs'
    
    login_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    login_date = Column(DateTime, default=datetime.utcnow, primary_key=True)
    login_ip = Column(String(50))
    device_info = Column(String(255))
    status = Column(String(20))  # 'success' or 'failed'

    user = relationship('User', back_populates='login_logs')