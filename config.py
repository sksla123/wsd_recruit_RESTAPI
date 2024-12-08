from dotenv import load_dotenv
import os

load_dotenv()

class Config:
   # Database Configuration
    MYSQL_DB_URL = os.getenv('MYSQL_DB_URL')
    MYSQL_DB_PORT = os.getenv('MYSQL_DB_PORT')
    MYSQL_DB_USER = os.getenv('MYSQL_DB_USER')
    MYSQL_DB_PASSWORD = os.getenv('MYSQL_DB_PASSWORD')

    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_DB_USER}:{MYSQL_DB_PASSWORD}@{MYSQL_DB_URL}:{MYSQL_DB_PORT}/your_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 기존 코드 + JWT 관련 설정
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 15))  # 분 단위
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 7*24*60))  # 분 단위

    # 로깅 및 보안 설정
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    LOGIN_ATTEMPT_WINDOW = int(os.getenv('LOGIN_ATTEMPT_WINDOW', 30))  # 분 단위

    @classmethod
    def get_db_config(cls):
        return {
            'MySQL':{
                'url': cls.MySQL_DB_URL,
                'port': cls.MySQL_DB_PORT,
                'user': cls.MySQL_DB_USER,
                'passord': cls.MySQL_DB_PASSWORD
            },
            'Redis': {
                'url': cls.REDIS_DB_URL,
                'port': cls.REDIS_DB_PORT,
                'passord': cls.REDIS_DB_PASSWORD
            },
            
        }