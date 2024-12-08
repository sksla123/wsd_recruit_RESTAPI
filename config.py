from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.getenv('MySQL_DB_USER')}:{os.getenv('MySQL_DB_PASSWORD')}@{os.getenv('MySQL_DB_URL')}:{os.getenv('MySQL_DB_PORT')}/your_database_name"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 3600 # 1시간
    JWT_REFRESH_TOKEN_EXPIRES = 2592000 # 30일

    MySQL_DB_URL = os.getenv('MySQL_DB_URL')
    MySQL_DB_PORT = os.getenv('MySQL_DB_PORT')
    MySQL_DB_USER = os.getenv('MySQL_DB_USER')
    MySQL_DB_PASSWORD = os.getenv('MySQL_DB_PASSWORD')

    REDIS_DB_URL = os.getenv('REDIS_DB_URL')
    REDIS_DB_PORT = os.getenv('REDIS_DB_PORT')
    REDIS_DB_PASSWORD = os.getenv('REDIS_DB_PASSWORD')

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