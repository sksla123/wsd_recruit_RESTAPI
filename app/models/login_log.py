from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .user import Base

class LoginLog(Base):
    __tablename__ = 'login_logs'
    
    login_id = Column(Integer, primary_key=True, autoincrement=True)
    login_date = Column(DateTime, default=datetime.utcnow)
    login_ip = Column(String(50))
    device_info = Column(String(255))
    status = Column(String(20))  # 'success' or 'failed'