from flask import jsonify, request
from app.services.auth_service import AuthService
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

class AuthController:
    @staticmethod
    def register():
        data = request.get_json()
        try:
            user = AuthService.register_user(data['email'], data['password'])
            return jsonify({"message": "User registered successfully"}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def login():
        data = request.get_json()
        user = AuthService.login_user(data['email'], data['password'])
        if user:
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
        return jsonify({"error": "Invalid credentials"}), 401

    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token), 200

    @staticmethod
    @jwt_required()
    def update_profile():
        user_id = get_jwt_identity()
        data = request.get_json()
        try:
            user = AuthService.update_user_profile(user_id, data)
            return jsonify({"message": "Profile updated successfully"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400