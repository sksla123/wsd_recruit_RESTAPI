from app.models import User, Login, LoginLog
from app import db
from app.utils.auth_util import hash_password, verify_password, generate_token, decode_token
from app.utils import responses
from flask import request
from datetime import datetime, timedelta

def register_user(data):
    """Registers a new user."""
    try:
        user_email = data.get('user_email')
        user_password = data.get('user_password')

        # Validate email format (using a simple regex - you might want a more robust validation)
        if not user_email or "@" not in user_email:
            return responses.error_response(400, "Invalid email format")

        # Check if user already exists
        existing_user = User.query.filter_by(user_email=user_email).first()
        if existing_user:
            return responses.error_response(400, "User already exists")

        # Hash the password
        hashed_password = hash_password(user_password)

        # Create a new user
        new_user = User(
            user_email=user_email,
            user_password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return responses.success_response(201, "User registered successfully")

    except Exception as e:
        print(f"Error registering user: {e}")
        return responses.error_response(500, "Failed to register user")


def login_user(data):
    """Logs in a user."""
    try:
        user_email = data.get('user_email')
        user_password = data.get('user_password')

        user = User.query.filter_by(user_email=user_email).first()
        if not user or not verify_password(user_password, user.user_password):
            # Log failed login attempt
            log_login_attempt(user_email, 'failed')
            return responses.error_response(401, "Invalid email or password")

        # Generate tokens
        access_token = generate_token(user.user_id, 'access')
        refresh_token = generate_token(user.user_id, 'refresh')

        # Store refresh token in the database
        login_entry = Login(
            refresh_token=refresh_token,
            user_id=user.user_id,
            device_info=request.user_agent.string  # Get device info from request headers
        )
        db.session.add(login_entry)

        # Update last login date for the user
        user.last_login_date = datetime.utcnow()
        db.session.commit()

        # Log successful login attempt
        log_login_attempt(user_email, 'success')

        return responses.token_response(200, "Login successful", access_token, refresh_token)

    except Exception as e:
        print(f"Error logging in user: {e}")
        return responses.error_response(500, "Failed to login user")


def refresh_token(data):
    """Refreshes the access token using the refresh token."""
    try:
        refresh_token = data.get('refresh_token')
        
        # Check if refresh token exists in the database
        login_entry = Login.query.filter_by(refresh_token=refresh_token).first()
        if not login_entry:
            return responses.error_response(401, 'Invalid refresh token')

        # Check if the refresh token is expired
        if login_entry.expired_date < datetime.utcnow():
            return responses.error_response(401, 'Refresh token expired')

        # Decode the refresh token to get the user ID
        try:
            user_id = decode_token(refresh_token)['sub']
        except Exception as e:
            print(f"Error decoding refresh token: {e}")
            return responses.error_response(401, 'Invalid refresh token')

        # Generate a new access token
        access_token = generate_token(user_id, 'access')

        return responses.token_response(200, 'Token refreshed successfully', access_token, refresh_token)

    except Exception as e:
        print(f"Error refreshing token: {e}")
        return responses.error_response(500, 'Failed to refresh token')


def update_user_profile(data):
    """Updates the user's profile."""
    try:
        # Get the user ID from the access token (using the auth_required decorator)
        user_id = decode_token(request.headers.get('Authorization').split(" ")[1])['sub']
        user = User.query.get(user_id)
        if not user:
            return responses.error_response(404, 'User not found')

        # Update password if provided
        new_password = data.get('user_password')
        if new_password:
            user.user_password = hash_password(new_password)

        # Update other profile fields as needed
        # ...

        db.session.commit()
        return responses.success_response(200, 'Profile updated successfully')

    except Exception as e:
        print(f"Error updating user profile: {e}")
        return responses.error_response(500, 'Failed to update profile')


def log_login_attempt(user_email, status):
    """Logs a login attempt to the LoginLog table."""
    try:
        login_log_entry = LoginLog(
            login_ip=request.remote_addr,
            device_info=request.user_agent.string,
            status=status
        )
        db.session.add(login_log_entry)
        db.session.commit()
    except Exception as e:
        print(f"Error logging login attempt: {e}")