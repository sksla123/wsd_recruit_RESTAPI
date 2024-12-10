from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Flask Configuation
    FLASK_BASE_URL = os.getenv('FLASK_BASE_URL')
    FLASK_PORT = os.getenv('FLASK_PORT')

    TIME_ZONE = os.getenv('TIMEZONE')

    # MySQL Configuration
    MySQL_DB_URL = os.getenv('MySQL_DB_URL')
    MySQL_DB_PORT = int(os.getenv('MySQL_DB_PORT'))
    MySQL_DB_USER = os.getenv('MySQL_DB_USER')
    MySQL_DB_PASSWORD = os.getenv('MySQL_DB_PASSWORD')
    MySQL_DB_NAME = os.getenv('MySQL_DB_NAME')

    # Redis Configuration (현재 사용하지 않음)
    REDIS_DB_URL = os.getenv('REDIS_DB_URL')
    REDIS_DB_PORT = int(os.getenv('REDIS_DB_PORT'))
    REDIS_DB_PASSWORD = os.getenv('REDIS_DB_PASSWORD')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))  # minutes
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES'))  # minutes

    # Database URI for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MySQL_DB_USER}:{MySQL_DB_PASSWORD}@{MySQL_DB_URL}:{MySQL_DB_PORT}/{MySQL_DB_NAME}?charset=utf8mb4"  # 쿼리 매개변수 추가
    SQLALCHEMY_TRACK_MODIFICATIONS = False