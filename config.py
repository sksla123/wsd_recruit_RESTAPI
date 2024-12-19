from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

def string_to_bool(s):
    if s.lower() in ['true', '1', 't', 'y', 'yes']:
        return True
    elif s.lower() in ['false', '0', 'f', 'n', 'no']:
        return False
    else:
        raise ValueError(f"Invalid literal for boolean: {s}")

class Config:
    # Flask Configuration
    FLASK_BASE_URL = os.getenv('FLASK_BASE_URL', '127.0.0.1')
    FLASK_PORT = os.getenv('FLASK_PORT', '5000')
    FLASK_DEBUG_MODE = string_to_bool(os.getenv('FLASK_DEBUG_MODE', 'False'))

    # MySQL Configuration
    MySQL_DB_URL = os.getenv('MySQL_DB_URL', 'localhost')
    MySQL_DB_PORT = int(os.getenv('MySQL_DB_PORT', '3306'))
    MySQL_DB_USER = os.getenv('MySQL_DB_USER', 'root')
    MySQL_DB_PASSWORD = os.getenv('MySQL_DB_PASSWORD', '')
    MySQL_DB_NAME = os.getenv('MySQL_DB_NAME', 'WSDa3')

    # Redis Configuration (현재 사용하지 않음)
    REDIS_DB_URL = os.getenv('REDIS_DB_URL', 'localhost')
    REDIS_DB_PORT = int(os.getenv('REDIS_DB_PORT', '6379'))
    REDIS_DB_PASSWORD = os.getenv('REDIS_DB_PASSWORD', '')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '15')))  # 기본 15분
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', '1440')))  # 기본 24시간

    # Database URI for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MySQL_DB_USER}:{MySQL_DB_PASSWORD}@{MySQL_DB_URL}:{MySQL_DB_PORT}/{MySQL_DB_NAME}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
