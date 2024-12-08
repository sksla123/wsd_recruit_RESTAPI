from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base

class Login(Base):
    __tablename__ = 'logins'
    
    refresh_token = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    device_info = Column(String(255))
    created_date = Column(DateTime, default=datetime.utcnow)
    expired_date = Column(DateTime)

    user = relationship("User")