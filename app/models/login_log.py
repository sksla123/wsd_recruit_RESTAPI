from app.models.user import db
from datetime import datetime

class LoginLog(db.Model):
    __tablename__ = 'LoginLog'
    login_date = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_ip = db.Column(db.String(255))
    device_info = db.Column(db.String(255))
    status = db.Column(db.String(255))  # 'success' or 'failed'

    def __repr__(self):
        return f'<LoginLog {self.login_id}>'