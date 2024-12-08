from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    user_authority = db.Column(db.String(255), default='user')  # 'user' or 'admin'
    user_password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_bookmark = db.Column(db.Text)  # comma-separated list of poster_ids
    user_applicated = db.Column(db.Text)  # comma-separated list of poster_ids
    last_login_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.user_email}>'