from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_authority = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_bookmark = db.Column(db.Text)
    user_applicated = db.Column(db.Text)