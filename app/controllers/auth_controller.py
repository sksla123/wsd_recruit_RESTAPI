from flask import request, jsonify
from app.services.auth_service import AuthService
from app.utils.validator import Validator

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def register(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # 이메일 및 비밀번호 검증
        if not Validator.validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        
        if not Validator.validate_password(password):
            return jsonify({"error": "Invalid password format"}), 400

        user = self.auth_service.register(email, password)
        
        if user:
            return jsonify({"message": "User registered successfully"}), 201
        else:
            return jsonify({"error": "User already exists"}), 409

    def login(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        ip_address = request.remote_addr
        device_info = request.user_agent.string

        access_token, refresh_token = self.auth_service.login(
            email, password, ip_address, device_info
        )

        if access_token and refresh_token:
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401