# models/__init__.py
from sqlalchemy.ext.declarative import declarative_base

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

# Base 클래스 생성
Base = declarative_base()

from .company_group import CompanyGroup
from .company import Company
from .user_level import UserLevel