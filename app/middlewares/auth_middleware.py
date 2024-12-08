from functools import wraps
from flask import request
from app.utils.auth_util import decode_token
from app.utils import responses

def auth_required(f):
    """Decorator for protecting routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return responses.error_response(401, 'Authorization token missing')

        try:
            # Decode the token to get user information
            data = decode_token(token)
            # You can access user ID from data['sub'] if needed
        except Exception as e:
            print(f"Error decoding token: {e}")
            return responses.error_response(401, 'Invalid token')

        return f(*args, **kwargs)

    return decorated