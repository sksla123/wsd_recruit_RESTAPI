import os
from dotenv import load_dotenv
from .util import load_from_pickle, base64_encode, base64_decode, now_korea, get_latest_file_paths
from .scrap import JobCodeTable, CodeTable, startWebScrapping

import json
import pymysql
import pandas as pd

# .env 파일 로드
load_dotenv()

class DBInitializer:
    """
    데이터베이스 초기화 클래스

    .env 파일에서 데이터베이스 연결 정보를 읽어와 연결을 생성하고,
    테이블을 생성하는 등의 초기화 작업을 수행합니다.
    """
    def __init__(self, code_table=None, job_data=None, code_table_pkl_file_path=None, job_data_pkl_file_path=None):
        """
        DBInitializer 객체를 초기화합니다.

        Args:
            code_table_pkl_file_path (str): 코드 테이블 pickle 파일 경로
            job_data_pkl_file_path (str): 직업 데이터 pickle 파일 경로
        """
        if job_data is not None and job_data_pkl_file_path is not None:
            raise

        if code_table is not None and code_table_pkl_file_path is not None:
            raise

        self._code_table = code_table
        self._job_data = job_data
        
        self.scrap_base_url = "https://www.saramin.co.kr"
        
        self.db_url = os.getenv("MySQL_DB_URL")
        # self._db_port = os.getenv("MySQL_DB_PORT")
        self.db_port = int(os.getenv("MySQL_DB_PORT"))  # 포트 번호는 정수형으로 변환
        self.db_user = os.getenv("MySQL_DB_USER")
        self.db_password = os.getenv("MySQL_DB_PASSWORD")
        self.db_name = os.getenv("MySQL_DB_NAME")
        self.admin_password = os.getenv("ADMIN_PASSWORD")
        
        self.code_table_pkl_file_path = code_table_pkl_file_path
        self.job_data_pkl_file_path = job_data_pkl_file_path

        self.force_creation = False

        self.mydb = self.connect_to_db()
        self.mycursor = self.mydb.cursor()

        self.process_job_data()

    def set_force_create_table(self, flag = False):
        self.force_creation = flag
        
    def process_job_data(self):
        if self.code_table_pkl_file_path is not None:
            self.code_table = load_from_pickle(self.code_table_pkl_file_path)
        else:
            self.code_table = self._code_table

        if self.job_data_pkl_file_path is not None:
            job_data = load_from_pickle(self.job_data_pkl_file_path)
        else:
            job_data = self._job_data

        self.salcode2sal = ['회사내규에 따름', 
                       '면접 후 결정', 
                       '2400만원 이상', 
                       '2600만원 이상', 
                       '2800만원 이상', 
                       '3000만원 이상', 
                       '3200만원 이상', 
                       '3400만원 이상', 
                       '3600만원 이상', 
                       '3800만원 이상', 
                       '4000만원 이상', 
                       '5000만원 이상', 
                       '6000만원 이상', 
                       '7000만원 이상', 
                       '8000만원 이상', 
                       '9000만원 이상',
                       '1억원 이상']
        
        self.educode2edu = ['학력무관', '고졸', '대학(2,3년)', '대학교(4년)', '석사', '박사']

        loc_code_table = pd.merge(self.code_table.total_loc, self.code_table.loc_1, on='1차 지역코드', how='left')
        loc_code_table.drop('2차 지역코드', axis=1, inplace=True)
        loc_code_table.rename(columns={'지역코드': 'loc_code', '지역명': 'loc_name', '1차 지역코드': 'loc_mcode', '1차 지역명': 'loc_mname'}, inplace=True)
        self.loc_code_table = loc_code_table

        job_code_table = self.code_table.jobCodeTable.get_total_dataframe()[['직무 코드', '직무 키워드명']]
        job_code_table.rename(columns = {'직무 코드': 'job_code', '직무 키워드명': 'job_name'}, inplace=True)
        self.job_code_table = job_code_table
        
        corrupted_datas = []
        
        groups = set()
        self.company2group = dict()
        self.company2complink = dict()
        
        companys = set()
        
        # 튜플 값이 들어감
        self.jobPostingJob = set()
        self.jobPostingLoc = set()

        self.userLevelCode2userLevelName = {0: "administrator", 5: "company_user", 10: "normal_user"}

        self.job_data = {}
        for key in job_data.keys():
            data = job_data[key]
        
            poster_id = key
            company_name = data.get("company_name") # not nullable 
            company_href = data.get("company_href") # nullable
            main_corp = data.get("main_corp") # nullable
            job_title = data.get("job_title") # not nullable
            job_href = data.get("job_href") # not nullable
            job_sectors = data.get("job_sectors") # nullable
            work_place = data.get("work_place") # nullable
            career = data.get("career") # nullable
            education = data.get("education") # nullable
            edu_code = data.get("edu_code") # not nullable
            edu_upper = data.get("edu_upper") # nullable
            deadline = data.get("deadline") # not nullable
            registered_days = data.get("registered_days") # not nullable
            loc_code = data.get("loc_code") # not empty
            job_code = data.get("job_code") # not empty
            sal_code = data.get("sal_code") # not nullable
        
            # Check not nullable fields
            not_nullable_fields = [company_name, job_title, edu_code, deadline, registered_days, sal_code]
            if any(field is None for field in not_nullable_fields):
                corrupted_datas.append(poster_id)
                continue
        
            # Check not empty fields
            if not loc_code or not job_code:
                corrupted_datas.append(poster_id)
                continue

            if main_corp is not None:
                groups.add(main_corp)
                self.company2group[company_name] = main_corp

            if company_href is not None and self.scrap_base_url not in company_href:
                self.company2complink[company_name] = self.scrap_base_url + company_href

            if self.scrap_base_url not in job_href:
                data["job_href"] = self.scrap_base_url + job_href
        
            companys.add(company_name)
        
            for _job_code in job_code:
                self.jobPostingJob.add((poster_id, _job_code))
        
            for _loc_code in loc_code:
                self.jobPostingLoc.add((poster_id, _loc_code))

            self.job_data[key] = data
            
        self.groups = list(groups)
        self.companys = list(companys)

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

    def _drop_database(self):
        try:
            # 현재 데이터베이스 연결 종료
            self.close_connection()
            
            # 데이터베이스 없이 연결
            temp_db = pymysql.connect(
                host=self.db_url,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password
            )
            temp_cursor = temp_db.cursor()
            
            # 데이터베이스 삭제
            temp_cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            temp_db.commit()
            
            print(f"데이터베이스 {self.db_name}가 삭제되었습니다.")
            
            # 임시 연결 종료
            temp_cursor.close()
            temp_db.close()
        except pymysql.Error as err:
            print(f"데이터베이스 삭제 중 오류 발생: {err}")
            raise
    
    def _create_database(self):
        try:
            # 데이터베이스 없이 연결
            temp_db = pymysql.connect(
                host=self.db_url,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password
            )
            temp_cursor = temp_db.cursor()
            
            # 데이터베이스 생성
            temp_cursor.execute(f"CREATE DATABASE {self.db_name}")
            temp_db.commit()
            
            print(f"데이터베이스 {self.db_name}가 생성되었습니다.")
            
            # 임시 연결 종료
            temp_cursor.close()
            temp_db.close()
            
            # 새로운 데이터베이스로 재연결
            self.mydb = self.connect_to_db()
            self.mycursor = self.mydb.cursor()
        except pymysql.Error as err:
            print(f"데이터베이스 생성 중 오류 발생: {err}")
            raise

    
    def create_table(self, table_name, sql_query):
        """
        force_creation 플래그에 따라 테이블을 생성합니다.
        
        Args:
            table_name (str): 생성할 테이블 이름
            sql_query (str): 테이블 생성 SQL 쿼리
        """
        try:
            if self.force_creation:
                # 테이블이 이미 존재하는 경우 삭제
                self.mycursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"기존 {table_name} 테이블을 삭제했습니다.")

            # 테이블 생성
            self.mycursor.execute(sql_query)
            self.mydb.commit()
            print(f"{table_name} 테이블이 생성되었습니다.")
        except pymysql.Error as err:
            print(f"{table_name} 테이블 생성 오류: {err}")
            raise

    def close_connection(self):
        """
        DB와 연결을 종료합니다.
        """
        try:
            if self.mycursor:
                self.mycursor.close()
                print("DB 커서가 닫혔습니다.")
            if self.mydb:
                self.mydb.close()
                print("DB 연결이 닫혔습니다.")
        except pymysql.Error as err:
            print(f"DB 연결 종료 중 오류: {err}")
            raise

    def _create_group_table(self):
        """
        Group 테이블을 생성합니다. force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE CompanyGroup (
            group_id INT AUTO_INCREMENT PRIMARY KEY,
            group_name VARCHAR(255)
        ) ENGINE=InnoDB
        """
        self.create_table("CompanyGroup", sql_query)

    def create_and_init_group_table(self):
        """
        Group 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            # Group 테이블 생성
            self._create_group_table()

            # Group 데이터 삽입
            if not self.groups:
                print("초기화할 그룹 데이터가 없습니다.")
                return

            insert_query = "INSERT INTO CompanyGroup (group_name) VALUES (%s)"
            group_data = [(group_name,) for group_name in self.groups]

            self.mycursor.executemany(insert_query, group_data)
            self.mydb.commit()

            print(f"Group 테이블에 {len(self.groups)}개의 그룹 데이터가 삽입되었습니다.")
        except pymysql.Error as err:
            print(f"Group 테이블 초기화 오류: {err}")
            raise

            print(f"Group 테이블에 {len(self.groups)}개의 그룹 데이터가 삽입되었습니다.")
        except pymysql.Error as err:
            print(f"Group 테이블 초기화 오류: {err}")
            raise

    def _create_company_table(self):
        """
        Company 테이블을 생성합니다. force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE Company (
            comp_id INT AUTO_INCREMENT PRIMARY KEY,
            comp_name VARCHAR(255) NOT NULL,
            comp_link VARCHAR(255),
            group_id INT,
            FOREIGN KEY (group_id) REFERENCES CompanyGroup(group_id) ON DELETE SET NULL
        ) ENGINE=InnoDB
        """
        self.create_table("Company", sql_query)

    def create_and_init_company_table(self):
        """
        Company 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            self._create_company_table()
            if not self.companys:
                print("초기화할 회사 데이터가 없습니다.")
                return
            insert_query = """
            INSERT INTO Company (comp_name, comp_link, group_id)
            VALUES (%s, %s, %s)
            """
            company_data = []
            for company_name in self.companys:
                comp_link = self.company2complink.get(company_name)
                group_name = self.company2group.get(company_name)
                group_id = None
                if group_name and group_name in self.groups:
                    group_id_query = "SELECT group_id FROM CompanyGroup WHERE group_name = %s"
                    self.mycursor.execute(group_id_query, (group_name,))
                    result = self.mycursor.fetchone()
                    if result:
                        group_id = result[0]
                company_data.append((company_name, comp_link, group_id))
            self.mycursor.executemany(insert_query, company_data)
            self.mydb.commit()
            print(f"Company 테이블에 {len(self.companys)}개의 회사 데이터가 삽입되었습니다.")
        except pymysql.Error as err:
            print(f"Company 테이블 초기화 오류: {err}")
            raise

    def _create_salcode_table(self):
        """
        SalCode 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE SalCode (
            sal_code INT PRIMARY KEY,
            sal_name VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB
        """
        self.create_table("SalCode", sql_query)
    
    def create_and_init_salcaode_table(self):
        """
        SalCode 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            # SalCode 테이블 생성
            self._create_salcode_table()
    
            # SalCode 데이터 삽입
            if not self.salcode2sal:
                print("초기화할 급여 코드 데이터가 없습니다.")
                return
    
            insert_query = "INSERT INTO SalCode (sal_code, sal_name) VALUES (%s, %s)"
            salcode_data = [(i, sal_name) for i, sal_name in enumerate(self.salcode2sal)]
    
            self.mycursor.executemany(insert_query, salcode_data)
            self.mydb.commit()
            print(f"SalCode 테이블에 {len(self.salcode2sal)}개의 급여 코드 데이터가 삽입되었습니다.")
    
        except pymysql.Error as err:
            print(f"SalCode 테이블 초기화 오류: {err}")
            raise

    def _create_educode_table(self):
        """
        EduCode 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE EduCode (
            edu_code INT PRIMARY KEY,
            edu_name VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB
        """
        self.create_table("EduCode", sql_query)
    
    def create_and_init_educode_table(self):
        """
        EduCode 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            # EduCode 테이블 생성
            self._create_educode_table()
    
            # EduCode 데이터 삽입
            if not self.educode2edu:
                print("초기화할 학력 코드 데이터가 없습니다.")
                return
    
            insert_query = "INSERT INTO EduCode (edu_code, edu_name) VALUES (%s, %s)"
            educode_data = [(i, edu_name) for i, edu_name in enumerate(self.educode2edu)]
    
            self.mycursor.executemany(insert_query, educode_data)
            self.mydb.commit()
            print(f"EduCode 테이블에 {len(self.educode2edu)}개의 학력 코드 데이터가 삽입되었습니다.")
    
        except pymysql.Error as err:
            print(f"EduCode 테이블 초기화 오류: {err}")
            raise

    def _create_jobcode_table(self):
        """
        JobCode 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE JobCode (
            job_code INT PRIMARY KEY,
            job_name VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB
        """
        self.create_table("JobCode", sql_query)
    
    def create_and_init_jobcode_table(self):
        """
        JobCode 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            # JobCode 테이블 생성
            self._create_jobcode_table()
    
            # JobCode 데이터 삽입
            if not hasattr(self, 'job_code_table') or self.job_code_table.empty:
                print("초기화할 직무 코드 데이터가 없습니다.")
                return
    
            insert_query = "INSERT INTO JobCode (job_code, job_name) VALUES (%s, %s)"
            jobcode_data = self.job_code_table[['job_code', 'job_name']].values.tolist()
    
            self.mycursor.executemany(insert_query, jobcode_data)
            self.mydb.commit()
            print(f"JobCode 테이블에 {len(jobcode_data)}개의 직무 코드 데이터가 삽입되었습니다.")
    
        except pymysql.Error as err:
            print(f"JobCode 테이블 초기화 오류: {err}")
            raise

    def _create_salcode_table(self):
        """
        SalCode 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE SalCode (
            sal_code INT PRIMARY KEY,
            sal_name VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB
        """
        self.create_table("SalCode", sql_query)
    
    def create_and_init_salcode_table(self):
        """
        SalCode 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            # SalCode 테이블 생성
            self._create_salcode_table()
    
            # SalCode 데이터 삽입
            if not self.salcode2sal:
                print("초기화할 급여 코드 데이터가 없습니다.")
                return
    
            insert_query = "INSERT INTO SalCode (sal_code, sal_name) VALUES (%s, %s)"
            salcode_data = [(i, sal_name) for i, sal_name in enumerate(self.salcode2sal)]
    
            self.mycursor.executemany(insert_query, salcode_data)
            self.mydb.commit()
            print(f"SalCode 테이블에 {len(self.salcode2sal)}개의 급여 코드 데이터가 삽입되었습니다.")
    
        except pymysql.Error as err:
            print(f"SalCode 테이블 초기화 오류: {err}")
            raise

    
    def _create_loccode_table(self):
        """
        LocCode 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE LocCode (
            loc_code INT PRIMARY KEY,
            loc_name VARCHAR(255) NOT NULL,
            loc_mcode INT,
            loc_mname VARCHAR(255)
        ) ENGINE=InnoDB
        """
        self.create_table("LocCode", sql_query)
    
    def create_and_init_loccode_table(self):
        """
        LocCode 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            # LocCode 테이블 생성
            self._create_loccode_table()
    
            # LocCode 데이터 삽입
            if self.loc_code_table.empty:
                print("초기화할 지역 코드 데이터가 없습니다.")
                return
    
            insert_query = """
            INSERT INTO LocCode (loc_code, loc_name, loc_mcode, loc_mname) 
            VALUES (%s, %s, %s, %s)
            """
            loccode_data = self.loc_code_table[['loc_code', 'loc_name', 'loc_mcode', 'loc_mname']].values.tolist()
    
            self.mycursor.executemany(insert_query, loccode_data)
            self.mydb.commit()
            print(f"LocCode 테이블에 {len(loccode_data)}개의 지역 코드 데이터가 삽입되었습니다.")
    
        except pymysql.Error as err:
            print(f"LocCode 테이블 초기화 오류: {err}")
            raise

    def _create_jobpostingjob_table(self):
        """
        JobPostingJob 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE JobPostingJob (
            poster_id VARCHAR(255),
            job_code INT,
            PRIMARY KEY (poster_id, job_code),
            FOREIGN KEY (poster_id) REFERENCES JobPosting(poster_id) ON DELETE CASCADE,
            FOREIGN KEY (job_code) REFERENCES JobCode(job_code) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
        self.create_table("JobPostingJob", sql_query)
    
    def create_and_init_jobpostingjob_table(self):
        """
        JobPostingJob 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            self._create_jobpostingjob_table()
    
            if not self.jobPostingJob:
                print("초기화할 JobPostingJob 데이터가 없습니다.")
                return
    
            insert_query = "INSERT INTO JobPostingJob (poster_id, job_code) VALUES (%s, %s)"
            self.mycursor.executemany(insert_query, list(self.jobPostingJob))
            self.mydb.commit()
            print(f"JobPostingJob 테이블에 {len(self.jobPostingJob)}개의 데이터가 삽입되었습니다.")
        except pymysql.Error as err:
            print(f"JobPostingJob 테이블 초기화 오류: {err}")
            raise
    
    def _create_jobpostingloc_table(self):
        """
        JobPostingLoc 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE JobPostingLoc (
            poster_id VARCHAR(255),
            loc_code INT,
            PRIMARY KEY (poster_id, loc_code),
            FOREIGN KEY (poster_id) REFERENCES JobPosting(poster_id) ON DELETE CASCADE,
            FOREIGN KEY (loc_code) REFERENCES LocCode(loc_code) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
        self.create_table("JobPostingLoc", sql_query)
    
    def create_and_init_jobpostingloc_table(self):
        """
        JobPostingLoc 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            self._create_jobpostingloc_table()
    
            if not self.jobPostingLoc:
                print("초기화할 JobPostingLoc 데이터가 없습니다.")
                return
    
            insert_query = "INSERT INTO JobPostingLoc (poster_id, loc_code) VALUES (%s, %s)"
            self.mycursor.executemany(insert_query, list(self.jobPostingLoc))
            self.mydb.commit()
            print(f"JobPostingLoc 테이블에 {len(self.jobPostingLoc)}개의 데이터가 삽입되었습니다.")
        except pymysql.Error as err:
            print(f"JobPostingLoc 테이블 초기화 오류: {err}")
            raise

    def _create_userlevel_table(self):
        """
        UserLevel 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE UserLevel (
            user_level INT PRIMARY KEY,
            user_level_name VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB
        """
        self.create_table("UserLevel", sql_query)
    
    def create_and_init_userlevel_table(self):
        """
        UserLevel 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            # UserLevel 테이블 생성
            self._create_userlevel_table()
    
            # UserLevel 데이터 삽입
            if not hasattr(self, 'userLevelCode2userLevelName') or not self.userLevelCode2userLevelName:
                print("초기화할 사용자 레벨 데이터가 없습니다.")
                return
    
            insert_query = "INSERT INTO UserLevel (user_level, user_level_name) VALUES (%s, %s)"
            userlevel_data = [(level, name) for level, name in self.userLevelCode2userLevelName.items()]
    
            self.mycursor.executemany(insert_query, userlevel_data)
            self.mydb.commit()
            print(f"UserLevel 테이블에 {len(userlevel_data)}개의 사용자 레벨 데이터가 삽입되었습니다.")
    
        except pymysql.Error as err:
            print(f"UserLevel 테이블 초기화 오류: {err}")
            raise

    def _create_user_table(self):
        """
        User 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE User (
            user_id VARCHAR(255) PRIMARY KEY,
            user_email VARCHAR(255) NOT NULL,
            user_level INT,
            user_password VARCHAR(255) NOT NULL,
            created_date DATETIME NOT NULL,
            last_updated_date DATETIME NOT NULL,
            user_bookmark JSON,
            user_applicated JSON,
            FOREIGN KEY (user_level) REFERENCES UserLevel(user_level)
        ) ENGINE=InnoDB
        """
        self.create_table("User", sql_query)
    
    def create_and_init_user_table(self):
        """
        User 테이블을 생성하고 초기 관리자 데이터를 삽입합니다.
        """
        try:
            # User 테이블 생성
            self._create_user_table()
    
            # 초기 관리자 데이터 삽입
            insert_query = """
            INSERT INTO User (user_id, user_email, user_level, user_password, created_date, last_updated_date, user_bookmark, user_applicated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            admin_data = (
                "admin",
                "admin12345@admin.com",
                0,
                base64_encode(self.admin_password),
                now_korea(),
                now_korea(),
                '{}',
                '{}'
            )
    
            self.mycursor.execute(insert_query, admin_data)
            self.mydb.commit()
            print("User 테이블에 초기 관리자 데이터가 삽입되었습니다.")
    
        except pymysql.Error as err:
            print(f"User 테이블 초기화 오류: {err}")
            raise

    def _create_jobposting_table(self):
        """
        JobPosting 테이블을 생성합니다.
        force_creation 플래그를 확인합니다.
        """
        sql_query = """
        CREATE TABLE JobPosting (
            comp_id INT NOT NULL,
            poster_id VARCHAR(255) PRIMARY KEY NOT NULL,
            poster_title VARCHAR(255) NOT NULL,
            poster_link VARCHAR(255) DEFAULT NULL,
            job_sectors VARCHAR(255) DEFAULT NULL,
            job_career VARCHAR(255) DEFAULT NULL,
            job_education VARCHAR(255) DEFAULT NULL,
            edu_code INT NOT NULL,
            edu_upper INT DEFAULT NULL,
            deadline_date DATE NOT NULL,
            last_updated_date DATE NOT NULL,
            job_codes JSON NOT NULL,
            loc_codes JSON NOT NULL,
            sal_code INT NOT NULL,
            poster_status INT NOT NULL,
            poster_writer_user_id VARCHAR(255) NOT NULL,
            view_cnts INT NOT NULL,
            FOREIGN KEY (comp_id) REFERENCES Company(comp_id),
            FOREIGN KEY (edu_code) REFERENCES EduCode(edu_code),
            FOREIGN KEY (sal_code) REFERENCES SalCode(sal_code),
            FOREIGN KEY (poster_writer_user_id) REFERENCES User(user_id)
        ) ENGINE=InnoDB;
        """
        self.create_table("JobPosting", sql_query)
    
    def create_and_init_jobposting_table(self):
        """
        JobPosting 테이블을 생성하고 데이터를 초기화합니다.
        """
        try:
            self._create_jobposting_table()
    
            if not self.job_data:
                print("초기화할 JobPosting 데이터가 없습니다.")
                return
    
            insert_query = """
            INSERT INTO JobPosting (
                comp_id, poster_id, poster_title, poster_link, job_sectors, job_career,
                job_education, edu_code, edu_upper, deadline_date, last_updated_date,
                job_codes, loc_codes, sal_code, poster_status, poster_writer_user_id, view_cnts
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    
            jobposting_data = []
            with open("./log.txt", "w", encoding="utf-8") as debug_file:
                for poster_id, data in self.job_data.items():
                    company_name = data.get("company_name")
                    comp_id = self._get_company_id(company_name)
                    
                    job_codes = json.dumps(list(data.get("job_code", set())), ensure_ascii=False)
                    loc_codes = json.dumps(sorted(list(data.get("loc_code", set()))), ensure_ascii=False)
    
                    record = (
                        comp_id,
                        poster_id,
                        data.get("job_title"),
                        data.get("job_href"),
                        json.dumps(data.get("job_sectors"), ensure_ascii=False),
                        data.get("career"),
                        data.get("education"),
                        data.get("edu_code"),
                        data.get("edu_upper"),
                        data.get("deadline"),
                        data.get("registered_days"),
                        job_codes,
                        loc_codes,
                        data.get("sal_code"),
                        1,  # poster_status
                        "admin",  # poster_writer_user_id
                        0 # view_cnts
                    )
                
                    print(f"DEBUG: {record}", file=debug_file)  # 디버깅 출력
                    jobposting_data.append(record)
                
            self.mycursor.executemany(insert_query, jobposting_data)
            self.mydb.commit()
            print(f"JobPosting 테이블에 {len(jobposting_data)}개의 데이터가 삽입되었습니다.")
    
        except pymysql.Error as err:
            print(f"JobPosting 테이블 초기화 오류: {err}")
            raise
    
    def _get_company_id(self, company_name):
        """
        회사 이름으로 회사 ID를 조회합니다.
        """
        query = "SELECT comp_id FROM Company WHERE comp_name = %s"
        self.mycursor.execute(query, (company_name,))
        result = self.mycursor.fetchone()
        return result[0] if result else None        

    def _create_user_bookmark_table(self):
        """
        UserBookmark 테이블을 생성합니다.
        """
        sql_query = """
        CREATE TABLE UserBookmark (
            user_id VARCHAR(255),
            poster_id VARCHAR(255),
            PRIMARY KEY (user_id, poster_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
            FOREIGN KEY (poster_id) REFERENCES JobPosting(poster_id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
        self.create_table("UserBookmark", sql_query)

    def _create_user_applicated_table(self):
        """
        UserApplicated 테이블을 생성합니다.
        """
        sql_query = """
        CREATE TABLE UserApplicated (
            application_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            poster_id VARCHAR(255),
            application TEXT,
            application_status INT,
            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
            FOREIGN KEY (poster_id) REFERENCES JobPosting(poster_id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
        self.create_table("UserApplicated", sql_query)

    def _create_user_applicated_log_table(self):
        """
        UserApplicatedLog 테이블을 생성합니다.
        """
        sql_query = """
        CREATE TABLE UserApplicatedLog (
            application_log_id INT AUTO_INCREMENT PRIMARY KEY,
            application_id INT,
            applicated_at DATETIME,
            user_id VARCHAR(255),
            poster_id VARCHAR(255),
            applicate_action INT,
            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
            FOREIGN KEY (poster_id) REFERENCES JobPosting(poster_id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
        self.create_table("UserApplicatedLog", sql_query)

    def _create_login_table(self):
        """
        Login 테이블을 생성합니다.
        """
        sql_query = """
        CREATE TABLE Login (
            refresh_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            refresh_token TEXT,
            created_at DATETIME,
            expires_at DATETIME,
            login_device_info TEXT,
            login_ip VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
        self.create_table("Login", sql_query)

    def _create_login_log_table(self):
        """
        LoginLog 테이블을 생성합니다.
        """
        sql_query = """
        CREATE TABLE LoginLog (
            login_log_id INT AUTO_INCREMENT PRIMARY KEY,
            login_date DATETIME,
            login_id VARCHAR(255),
            login_ip VARCHAR(255),
            login_device_info TEXT,
            login_success INT,
            FOREIGN KEY (login_id) REFERENCES User(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
        self.create_table("LoginLog", sql_query)

    def create_all_additional_tables(self):
        """
        추가된 5개의 테이블을 생성합니다.
        """
        try:
            self._create_user_bookmark_table()
            self._create_user_applicated_table()
            self._create_user_applicated_log_table()
            self._create_login_table()
            self._create_login_log_table()
            print("추가 테이블들이 성공적으로 생성되었습니다.")
        except pymysql.Error as err:
            print(f"추가 테이블 생성 중 오류 발생: {err}")
            raise

    def create_and_init_all_tables(self):
        """
        모든 테이블을 적절한 순서로 생성하고 초기화합니다.
        force_creation이 True일 경우 데이터베이스를 재생성합니다.
        """
        try:
            if self.force_creation:
                self._drop_database()
                self._create_database()

            # 1. 독립적인 테이블 생성 및 초기화
            self.create_and_init_group_table()
            self.create_and_init_salcode_table()
            self.create_and_init_educode_table()
            self.create_and_init_jobcode_table()
            self.create_and_init_loccode_table()
            self.create_and_init_userlevel_table()

            # 2. 외래 키 참조가 있는 테이블 생성 및 초기화
            self.create_and_init_company_table()
            self.create_and_init_user_table()

            # 3. JobPosting 테이블 생성
            self.create_and_init_jobposting_table()

            # 4. 다대다 관계 테이블 생성 및 초기화
            self.create_and_init_jobpostingjob_table()
            self.create_and_init_jobpostingloc_table()

            # 5. 추가 테이블 생성 (초기 데이터 없음)
            self.create_all_additional_tables()

            print("모든 테이블이 성공적으로 생성되고 초기화되었습니다.")
        except pymysql.Error as err:
            print(f"테이블 생성 및 초기화 중 오류 발생: {err}")
            raise

def initDB():
    # Jupyter Notebook 환경인지 확인
    if '__file__' in globals():
        # 일반 Python 스크립트에서는 __file__ 사용
        current_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        # Jupyter Notebook 환경에서는 os.getcwd() 사용
        current_dir = os.getcwd()
    
    # data 디렉토리 경로 결합
    dir_path = os.path.join(current_dir, "data")

    code_table_pkl_path, job_data_pkl_path = get_latest_file_paths(dir_path)
    print("코드테이블 피클 파일 경로:", code_table_pkl_path)
    print("잡데이터 피클 파일 경로:", job_data_pkl_path)
    
    db_initializer = DBInitializer(code_table_pkl_file_path=code_table_pkl_path, job_data_pkl_file_path=job_data_pkl_path)
    db_initializer.set_force_create_table(True)
    db_initializer.create_and_init_all_tables()

    db_initializer.set_force_create_table()
    
if __name__ == '__main__':
    initDB()