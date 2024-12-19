## !!! 빠른 배포를 위한 도커 이미지 제작 중 !!!


## 프로그램 사용법
### 0. Working directory를 프로젝트 최상단 폴더로 이동하세요.
: run.py가 위치한 폴더가 프로젝트 최상단 폴더입니다.

### 1. pip, conda와 같은 파이썬 패키지 매니저를 통해 프로그램 구동에 필요한 requirements를 다운받으세요.
현재 conda(파이썬 버전 3.12) 기준 등봉된 conda_py312_requirements.txt파일을 통해 설치할 수 있습니다. 
```
// conda 환경 설치 명령어 예시
// 설치시 conda-forge 채널을 추가할 것
conda install --file conda_py312_requirements.txt -c conda-forge
```

이후 모든 작업은 requirements가 설치된 환경에서 진행해야 합니다.

### 2. .env를 작성하세요. 
아래는 작성 예시입니다. .env 파일에는 민감한 정보가 포함될 수 있으므로 유출되지 않도록 조심하세요.
```
#/.env
FLASK_BASE_URL=127.0.0.1 # 이 애플리케이션에 접속할 주소
FLASK_PORT=5000 # 이 애플리케이션이 할당받을 포트
FLASK_DEBUG_MODE=False # 플라스크 디버그 모드 활성화 여부

MySQL_DB_URL=127.0.0.1 # MySQL에 접속할 수 있는 ip(또는 url)
MySQL_DB_PORT=3306 # MySQL에 접속할 수 있는 포트
MySQL_DB_USER=root # MySQL 사용자
MySQL_DB_PASSWORD=your-mysql-user-password # MySQL 사용자 비밀번호(없는 경우 생략)
MySQL_DB_NAME=WSDa3 # MySQL DB

REDIS_DB_URL=127.0.0.1 # Redis DB ip
REDIS_DB_PORT=6379 # Redis DB port
REDIS_DB_PASSWORD=your-redis-user-password # Redis DB 비밀번호(없는 경우 생략)

# JWT Configuration
JWT_SECRET_KEY=your-secret-key # JWT 비밀번호, 20글자 이상 설정할 것
JWT_ACCESS_TOKEN_EXPIRES=15 # JWT 토큰 엑세스 만료 기간 (분 단위)
JWT_REFRESH_TOKEN_EXPIRES=1440 # JWT 리프레쉬 토큰 만료 기간 (분 단위)

# 애플리케이션 초기 어드민 계정 비밀번호
ADMIN_PASSWORD = your-admin-password 
``` 

### (선택사항) 3. 초기 데이터 생성
미리 구축된 DB 또는 데이터가 존재하지 않는 경우 init_database_by_web_scrapping 폴더의 scrap.py와 DB_init.py파일을 통해 데이터 생성 및 DB 구축을 실행할 수 있습니다.

### (선택사항) 3-1. 크롤링 데이터가 아예 없는 경우
: 웹크롤링을 통해 데이터를 생성할 수 있습니다.

**(선택사항) 3-1.1. 웹 크롤러 실행하기**
! 시간이 굉장히 오래 걸릴 수 있습니다. (테스트 모드가 따로 있습니다.)
```
python -m init_database_by_web_scrapping.scrap
python -m init_database_by_web_scrapping.scrap --isTest // 테스트 모드로 실행하기(데이터가 제한됩니다.)
```

**(선택사항) 3-1.2. 생성된 결과물은 ./init_database_by_web_scrapping/data 폴더 안에 저장됩니다.**
```
init_database_by_web_scrapping/
├── data/
│   ├── 20241231000000_codetable_data_backup.pkl # 날짜는 예시
│   ├── 20241231000000_data_backup.pkl # 날짜는 예시시
```
codetable_data_backup 파일: 코드 테이블 정보가 저장된 파일입니다.
data_backup 파일: 잡포스터 정보가 저장된 파일입니다.

### (선택사항) 3-2. 크롤링 데이터가 있는 경우
**(선택사항) 3-2.1. 아래 명령어를 통해 MySQL DB를 초기화할 수 있습니다.**
! 반드시 MySQL이 실행된 상태여야 합니다.
```
python -m init_database_by_web_scrapping.DB_init
```

이 명령어를 실행할 경우 자동으로 init_database_by_web_scrapping/data 폴더에서 가장 최근에 생성된 파일을 선택합니다.

**만약 특정 파일을 실행시키게 하고 싶다면 해당 파일명을 아래처럼 수정하세요.**
```
20241231000000_codetable_data_backup.pkl -> selected_codetable_data_backup.pkl # 날짜는 예시
20241231000000_data_backup.pkl -> selected_data_backup.pkl # 날짜는 예시
```

### 4. 아래 명령어를 통해 application을 실행하세요.
```
python -m run
```

! 실행과 관련된 문의가 있는 경우 issue에 글을 남겨주시면 확인하겠습니다.

## 프로그램 설명
사람인 데이터를 기반으로 채용/공고 사이트를 모방한 백엔드 API입니다.

## 각 함수 설명 
: (Swagger 문서 참조(라우트: /api-docs))
![Screenshot-20241219225554](https://github.com/user-attachments/assets/05f9b1d9-c5c6-4a8f-9c7b-02459b210d41)

### AUTH, 사용자 및 인증 관련 api
```
**POST :/auth/login**
로그인을 처리합니다

**POST :/auth/logout**
로그아웃을 처리합니다(로그인 필요)

**PUT :/auth/profile**
회원정보를 수정합니다(로그인 필요)

**POST :/auth/refresh**
액세스 토큰을 갱신합니다

**POST :/auth/register**
회원 가입을 처리합니다
```
### APPLICATION, 지원서 관련 api
```
**PUT :/applications/**
지원 신청 내용을 업데이트 합니다(로그인 필요)

**POST :/applications/**
지원 신청을 처리합니다(로그인 필요)

**GET :/applications/**
사용자가 제출한 지원서를 조회합니다(로그인 필요)

**GET :/applications/logs**
지원 로그를 조회합니다(로그인 필요)

**DELETE :/applications/{application_id}**
지원을 취소합니다(로그인 필요)
```
### JOB, 채용 공고 관련 api
```
**GET :/jobs/**
채용 공고 목록을 조회합니다

**GET: /jobs/{poster_id}**
특정 채용 공고를 조회합니다
```
### BOOKMARK, 사용자 북마크 관련 api
```
**GET :/bookmarks/**
북마크 목록을 조회합니다(로그인 필요)

**POST :/bookmarks/{poster_id}**
해당 포스터를 북마크 등록/해제 합니다(로그인 필요)
```
### META, 코드화 된 데이터 해석에 필요한 기타 메타 정보를 획득할 수 있는 테이블
```
**GET :/metas/edu**
메타 테이블 중 education 목록을 조회합니다

**GET :/metas/job**
메타 테이블 중 job 테이블 목록을 조회합니다

**GET :/metas/job/{job_code}**
job_code를 통해 job_name을 획득합니다

**GET :/metas/loc**
메타 테이블 중 location 테이블 목록을 조회합니다

**GET :/metas/loc/{loc_code}**
loc code를 통해 해당 지역 정보를 획득득합니다

**GET :/metas/salary**
메타 테이블 중 salary Table 목록을 조회합니다
```

**! Swagger를 통해 테스트 시 JWT access token을 Authorize에 등록하면 편하게 테스트가 가능합니다!**