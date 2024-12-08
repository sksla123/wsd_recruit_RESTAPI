from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class Config:
    # Database Configuration
    MYSQL_DB_URL = os.getenv('MySQL_DB_URL', 'mysql://localhost')
    MYSQL_DB_PORT = os.getenv('MySQL_DB_PORT', '3306')
    MYSQL_DB_USER = os.getenv('MySQL_DB_USER')
    MYSQL_DB_PASSWORD = os.getenv('MySQL_DB_PASSWORD')
    MYSQL_DB_NAME = os.getenv('MySQL_DB_NAME')

    # Redis Configuration
    REDIS_DB_URL = os.getenv('REDIS_DB_URL', 'localhost')
    REDIS_DB_PORT = os.getenv('REDIS_DB_PORT', '6379')
    REDIS_DB_PASSWORD = os.getenv('REDIS_DB_PASSWORD')

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MySQL_DB_USER')}:{os.getenv('MySQL_DB_PASSWORD')}@{os.getenv('MySQL_DB_URL')}:{os.getenv('MySQL_DB_PORT')}/{os.getenv('MySQL_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 15))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 3600))

    # Token Configurations
    ACCESS_TOKEN_DURATION = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES)
    REFRESH_TOKEN_DURATION = timedelta(hours=JWT_REFRESH_TOKEN_EXPIRES)
    
    @classmethod
    def get_db_config(cls):
        return {
            'MySQL': {
                'url': cls.MYSQL_DB_URL,
                'port': cls.MYSQL_DB_PORT,
                'user': cls.MYSQL_DB_USER,
                'password': cls.MYSQL_DB_PASSWORD,
                'database': cls.MYSQL_DB_NAME
            },
            'Redis': {
                'url': cls.REDIS_DB_URL,
                'port': cls.REDIS_DB_PORT,
                'password': cls.REDIS_DB_PASSWORD
            }
        }