import bcrypt
import jwt
from datetime import datetime, timedelta
from config import Config

def hash_password(password):
    """Hashes the password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    """Verifies the password against the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id, token_type):
    """Generates an access or refresh token."""
    payload = {
        'sub': user_id,
        'iat': datetime.utcnow(),
        'type': token_type
    }
    if token_type == 'access':
        payload['exp'] = datetime.utcnow() + timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRES)
    elif token_type == 'refresh':
        payload['exp'] = datetime.utcnow() + timedelta(minutes=Config.JWT_REFRESH_TOKEN_EXPIRES)

    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    """Decodes the token."""
    return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])