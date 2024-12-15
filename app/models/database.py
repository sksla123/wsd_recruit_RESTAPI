from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# 데이터베이스 URL 설정
MySQL_DB_URL = os.getenv('MySQL_DB_URL')
MySQL_DB_PORT = int(os.getenv('MySQL_DB_PORT'))
MySQL_DB_USER = os.getenv('MySQL_DB_USER')
MySQL_DB_PASSWORD = os.getenv('MySQL_DB_PASSWORD')
MySQL_DB_NAME = os.getenv('MySQL_DB_NAME')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MySQL_DB_USER}:{MySQL_DB_PASSWORD}@{MySQL_DB_URL}:{MySQL_DB_PORT}/{MySQL_DB_NAME}?charset=utf8mb4"

# 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

# 데이터베이스 세션을 얻는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()