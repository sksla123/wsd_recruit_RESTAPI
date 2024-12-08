from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    user_email = Column(String(255), unique=True, nullable=False)
    user_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    user_authority = Column(String(50), default='user')
    created_date = Column(DateTime, default=datetime.utcnow)
    last_updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_date = Column(DateTime, nullable=True)