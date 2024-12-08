from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.validators import validate_email_format, validate_password_strength
from sqlalchemy.orm import Session

auth_bp = Blueprint('auth', __name__)

class AuthController:
    def __init__(self, db_session: Session):
        self.auth_service = AuthService(db_session)

    def register(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not validate_email_format(email):
            return jsonify({"error": "Invalid email format"}), 400
        
        if not validate_password_strength(password):
            return jsonify({"error": "Weak password"}), 400

        try:
            user = self.auth_service.register_user(email, password)
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def login(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        ip_address = request.remote_addr
        device_info = request.user_agent.string

        access_token, refresh_token = self.auth_service.login_user(
            email, password, ip_address, device_info
        )

        if access_token and refresh_token:
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401