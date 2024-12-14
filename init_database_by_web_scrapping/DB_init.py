import os
from dotenv import load_dotenv
from .util import load_from_pickle
from .scrap import JobCodeTable, CodeTable
import pymysql

# .env 파일 로드
load_dotenv()

class DBInitializer:
    """
    데이터베이스 초기화 클래스

    .env 파일에서 데이터베이스 연결 정보를 읽어와 연결을 생성하고,
    테이블을 생성하는 등의 초기화 작업을 수행합니다.
    """
    def __init__(self, code_table_pkl_file_path, job_data_pkl_file_path):
        """
        DBInitializer 객체를 초기화합니다.

        Args:
            code_table_pkl_file_path (str): 코드 테이블 pickle 파일 경로
            job_data_pkl_file_path (str): 직업 데이터 pickle 파일 경로
        """
        self.db_url = os.getenv("MySQL_DB_URL")
        self.db_port = int(os.getenv("MySQL_DB_PORT"))  # 포트 번호는 정수형으로 변환
        self.db_user = os.getenv("MySQL_DB_USER")
        self.db_password = os.getenv("MySQL_DB_PASSWORD")
        self.db_name = os.getenv("MySQL_DB_NAME")
        self.code_table_pkl_file_path = code_table_pkl_file_path
        self.job_data_pkl_file_path = job_data_pkl_file_path

        self.mydb = self.connect_to_db()
        self.mycursor = self.mydb.cursor()

    def process_job_data(self):
        self.code_table = load_from_pickle(self.code_table_pkl_file_path)
        self.job_data = load_from_pickle(self.job_data_pkl_file_path)

        self.group_table = {}
        
        pass
        

    def connect_to_db(self):
        """
        데이터베이스에 연결합니다.

        Returns:
            pymysql.connections.Connection: 데이터베이스 연결 객체
        """
        try:
            mydb = pymysql.connect(
                host=self.db_url,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            print("데이터베이스 연결 성공")
            return mydb
        except pymysql.Error as err:
            print(f"데이터베이스 연결 오류: {err}")
            raise

    def create_table(self, table_name, sql_query):
        """
        테이블을 생성합니다.

        Args:
            table_name (str): 생성할 테이블 이름
            sql_query (str): 테이블 생성 SQL 쿼리
        """
        try:
            self.mycursor.execute(sql_query)
            self.mydb.commit()
            print(f"{table_name} 테이블이 생성되었습니다.")
        except pymysql.Error as err:
            print(f"{table_name} 테이블 생성 오류: {err}")
            raise

    def close_connection(self):
        """
        Group 테이블을 생성합니다.
        """
        try:
            # 테이블 생성 SQL 쿼리
            sql_query = """
            CREATE TABLE Group (
                group_id INT AUTO_INCREMENT PRIMARY KEY,
                group_name VARCHAR(255)
            )
            """
            self.mycursor.execute(sql_query)
            self.mydb.commit()
            print("Group 테이블이 생성되었습니다.")
        except pymysql.Error as err:
            print(f"Group 테이블 생성 오류: {err}")
            raise

    def _create_group_table(self):
        """
        Group 테이블을 생성합니다.
        """
        try:
            # 테이블 생성 SQL 쿼리 (ENGINE=InnoDB 추가)
            sql_query = """
            CREATE TABLE Group (
                group_id INT AUTO_INCREMENT PRIMARY KEY,
                group_name VARCHAR(255)
            ) ENGINE=InnoDB
            """
            self.mycursor.execute(sql_query)
            self.mydb.commit()
            print("Group 테이블이 생성되었습니다.")
        except pymysql.Error as err:
            print(f"Group 테이블 생성 오류: {err}")
            raise

    def create_and_init_group_table(self):
        
        pass