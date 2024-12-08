from app.models.user import db
from datetime import datetime, timedelta

class Login(db.Model):
    __tablename__ = 'Login'
    refresh_token = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    device_info = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    expired_date = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=365))  # Example: expires in 1 year

    def __repr__(self):
        return f'<Login {self.refresh_token}>'