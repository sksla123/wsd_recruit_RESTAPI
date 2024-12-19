# routes/bookmark_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import meta_service
from app.views.response import JsonResponse, fail # JsonResponse, success, fail import
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

meta = Namespace('meta', description='Meta data table related to api')

parser = meta.parser()
parser.add_argument('page', type=int, help='페이지 번호 (기본값: 1)', location='args', default=1)

@meta.route('/salary')
class GetSalaryTable(Resource):
    @meta.doc(
        security=None,
        description="메타 테이블 중 salary 테이블 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''
{
  "status": "success",
  "message": "조회에 성공했습니다.",
  "data": {
    "sal_codes": [
      {
        "sal_code": 0,
        "sal_name": "회사내규에 따름"
      },
      {
        "sal_code": 1,
        "sal_name": "면접 후 결정"
      },
      {
        "sal_code": 2,
        "sal_name": "2400만원 이상"
      },
      {
        "sal_code": 3,
        "sal_name": "2600만원 이상"
      },
      {
        "sal_code": 4,
        "sal_name": "2800만원 이상"
      },
      {
        "sal_code": 5,
        "sal_name": "3000만원 이상"
      },
      {
        "sal_code": 6,
        "sal_name": "3200만원 이상"
      },
      {
        "sal_code": 7,
        "sal_name": "3400만원 이상"
      },
      {
        "sal_code": 8,
        "sal_name": "3600만원 이상"
      },
      {
        "sal_code": 9,
        "sal_name": "3800만원 이상"
      },
      {
        "sal_code": 10,
        "sal_name": "4000만원 이상"
      },
      {
        "sal_code": 11,
        "sal_name": "5000만원 이상"
      },
      {
        "sal_code": 12,
        "sal_name": "6000만원 이상"
      },
      {
        "sal_code": 13,
        "sal_name": "7000만원 이상"
      },
      {
        "sal_code": 14,
        "sal_name": "8000만원 이상"
      },
      {
        "sal_code": 15,
        "sal_name": "9000만원 이상"
      },
      {
        "sal_code": 16,
        "sal_name": "1억원 이상"
      }
    ],
    "total_count": 17,
    "current_page": 1,
    "total_page": 1
  }
}''',
        }
    )
    def get(self):
        """
        메타 테이블 중 salary Table 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """

        try:
            success, data, message, status =  meta_service.get_salary_table(request.args.to_dict())
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@meta.route('/edu')
class GetEducationTable(Resource):
    @meta.doc(
        security=None,
        description="메타 테이블 education 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''{
  "status": "success",
  "message": "Education 테이블 조회에 성공했습니다.",
  "data": {
    "edu_codes": [
      {
        "edu_code": 0,
        "edu_name": "학력무관"
      },
      {
        "edu_code": 1,
        "edu_name": "고졸"
      },
      {
        "edu_code": 2,
        "edu_name": "대학(2,3년)"
      },
      {
        "edu_code": 3,
        "edu_name": "대학교(4년)"
      },
      {
        "edu_code": 4,
        "edu_name": "석사"
      },
      {
        "edu_code": 5,
        "edu_name": "박사"
      }
    ],
    "total_count": 6,
    "current_page": 1,
    "total_page": 1
  }
}''',
        }
    )
    def get(self):
        """
        메타 테이블 중 education 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        try:
            success, data, message, status =  meta_service.get_education_table(request.args.to_dict())
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
        
@meta.route('/job')
class GetJobTable(Resource):
    @meta.doc(
        security=None,
        description="메타 테이블 job 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''{
  "status": "success",
  "message": "job 테이블 조회에 성공했습니다.",
  "data": {
    "job_codes": [
      {
        "job_code": 80,
        "job_name": "게임개발"
      },
      {
        "job_code": 81,
        "job_name": "기술지원"
      },
      {
        "job_code": 82,
        "job_name": "데이터분석가"
      },
      {
        "job_code": 83,
        "job_name": "데이터엔지니어"
      },
      {
        "job_code": 84,
        "job_name": "백엔드/서버개발"
      },
      {
        "job_code": 85,
        "job_name": "보안컨설팅"
      },
      {
        "job_code": 86,
        "job_name": "앱개발"
      },
      {
        "job_code": 87,
        "job_name": "웹개발"
      },
      {
        "job_code": 88,
        "job_name": "웹마스터"
      },
      {
        "job_code": 89,
        "job_name": "유지보수"
      },
      {
        "job_code": 90,
        "job_name": "정보보안"
      },
      {
        "job_code": 91,
        "job_name": "퍼블리셔"
      },
      {
        "job_code": 92,
        "job_name": "프론트엔드"
      },
      {
        "job_code": 93,
        "job_name": "CISO"
      },
      {
        "job_code": 94,
        "job_name": "CPO"
      },
      {
        "job_code": 95,
        "job_name": "DBA"
      },
      {
        "job_code": 96,
        "job_name": "FAE"
      },
      {
        "job_code": 97,
        "job_name": "GM(게임운영)"
      },
      {
        "job_code": 98,
        "job_name": "IT컨설팅"
      },
      {
        "job_code": 99,
        "job_name": "QA/테스터"
      }
    ],
    "total_count": 2178,
    "current_page": 1,
    "total_page": 109
  }''',
        }
    )
    def get(self):
        """
        메타 테이블 중 job 테이블 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        try:
            success, data, message, status =  meta_service.get_job_table(request.args.to_dict())
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
        
@meta.route('/job/<int:job_code>')
class GetJobName(Resource):
    @meta.doc(
        security=None,
        params={
            'job_code': 'Job code, 이름을 알고 싶은 Job Code를 입력하세요.'
        },
        responses={
        200: '''{
  "status": "success",
  "message": "job name 조회에 성공했습니다.",
  "data": {
    "job_code": 80,
    "job_name": "게임개발"
  }
}''',
        400: '''{
  "status": "failed",
  "message": "JobCode not found",
  "data": {}
}'''
    })
    def get(self, job_code):
        """
        job_code를 통해 job_name을 획득합니다.
        """
        success, data, message, status = meta_service.get_job_name(job_code)
        return JsonResponse(success, data, message, status).to_response()
        
@meta.route('/loc')
class GetLocTable(Resource):
    @meta.doc(
        security=None,
        description="메타 테이블 location 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''{
  "status": "success",
  "message": "조회에 성공했습니다.",
  "data": {
    "loc_codes": [
      {
        "loc_code": 101000,
        "loc_name": "서울전체",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101010,
        "loc_name": "강남구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101020,
        "loc_name": "강동구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101030,
        "loc_name": "강북구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101040,
        "loc_name": "강서구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101050,
        "loc_name": "관악구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101060,
        "loc_name": "광진구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101070,
        "loc_name": "구로구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101080,
        "loc_name": "금천구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101090,
        "loc_name": "노원구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101100,
        "loc_name": "도봉구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101110,
        "loc_name": "동대문구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101120,
        "loc_name": "동작구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101130,
        "loc_name": "마포구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101140,
        "loc_name": "서대문구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101150,
        "loc_name": "서초구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101160,
        "loc_name": "성동구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101170,
        "loc_name": "성북구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101180,
        "loc_name": "송파구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      },
      {
        "loc_code": 101190,
        "loc_name": "양천구",
        "loc_mcode": 101000,
        "loc_mname": "서울"
      }
    ],
    "total_count": 664,
    "current_page": 1,
    "total_page": 34
  }
}''',
        }
    )
    def get(self):
        """
        메타 테이블 중 location 테이블 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        try:
            success, data, message, status =  meta_service.get_location_table(request.args.to_dict())
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
        
@meta.route('/loc/<int:loc_code>')
class GetLocData(Resource):
    @meta.doc(
        security=None,
        params={
            'loc_code': 'loc code, 상세 정보를 알고 싶은 loc code를 입력하세요.'
        },
        responses={
        200: '''{
  "status": "success",
  "message": "loc data 조회에 성공했습니다.",
  "data": {
    "loc_code": 101000,
    "loc_name": "서울전체",
    "loc_mcode": 101000,
    "loc_mname": "서울"
  }
}''',
        400: '''{
  "status": "failed",
  "message": "LocCode not found",
  "data": {}
}'''
    })
    def get(self, loc_code):
        """
        loc code를 통해 해당 지역 정보를 획득득합니다.
        """
        success, data, message, status = meta_service.get_loc_data(loc_code)
        return JsonResponse(success, data, message, status).to_response()