# routes/job_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import job_service
from app.views.response import JsonResponse, fail
from http import HTTPStatus

job = Namespace('job', description='poster related operations')

# Query parameters 모델 정의 (Swagger 문서화)
job_filters = job.model('JobFilters', {
    'title_contains': fields.String(example="Software Engineer"),  # 예시: title이 포함된 값
    'comp_id': fields.Integer(example=101),  # 예시: 특정 회사 ID
    'sal_code_eq': fields.Integer(example=3),  # 예시: salary code equals
    'sal_code_gte': fields.Integer(example=2),  # 예시: salary code greater than or equal to
    'sal_code_lte': fields.Integer(example=5),  # 예시: salary code less than or equal to
    'edu_code_eq': fields.Integer(example=1),  # 예시: education code equals
    'edu_code_gte': fields.Integer(example=2),  # 예시: education code greater than or equal to
    'edu_code_lte': fields.Integer(example=3),  # 예시: education code less than or equal to
    'deadline_date_eq': fields.String(example="2024-12-31"),  # 예시: 마감일이 특정 날짜인 값
    'deadline_date_gte': fields.String(example="2024-12-01"),  # 예시: 마감일이 이후인 값
    'deadline_date_lte': fields.String(example="2024-12-31"),  # 예시: 마감일이 이전인 값
    'loc_codes': fields.List(fields.Integer, example=[1, 2, 3]),  # 예시: 지역 코드 리스트
    'job_codes': fields.List(fields.Integer, example=[101, 102, 103]),  # 예시: 직업 코드 리스트
})

# 예시 데이터를 Swagger 문서에 등록
job.add_model('JobFilters', job_filters)

@job.route('/')
class Applications(Resource):
    """
    채용 공고 목록 관련 API
    """
    @job.doc(
        description="채용 공고 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
            'sort_by': '정렬 기준 (기본값: deadline_date)',
            'sort_order': '정렬 순서 (asc 또는 desc)',
            'title_contains': '제목을 포함한 검색어',
            'comp_id': '회사의 ID',
            'sal_code': '급여 코드 필터 (eq, gte, lte)',
            'edu_code': '학력 코드 필터 (eq, gte, lte)',
            'deadline_date': '마감일 필터 (eq, gte, lte)',
            'loc_codes': '위치 코드 필터 (리스트)',
            'job_codes': '직업 코드 필터 (리스트)'
        },
        responses={
            HTTPStatus.OK.value: {
                'description': '성공적인 응답',
                'examples': {
                    'application/json': {
                        "success": True,
                        "data": [
                            {
                                "poster_id": 1,
                                "title": "Python Developer",
                                "comp_id": 123,
                                "salary_code": 3,
                                "edu_code": 2,
                                "deadline": "2024-12-31",
                                "loc_code": [1, 2],
                                "job_code": [101],
                                "view_cnts": 25
                            },
                            {
                                "poster_id": 2,
                                "title": "Java Developer",
                                "comp_id": 124,
                                "salary_code": 4,
                                "edu_code": 3,
                                "deadline": "2024-12-31",
                                "loc_code": [1, 3],
                                "job_code": [102],
                                "view_cnts": 18
                            }
                        ],
                        "message": "채용 공고 목록을 성공적으로 조회했습니다.",
                        "status": 200
                    }
                }
            },
            HTTPStatus.BAD_REQUEST.value: {
                'description': '잘못된 요청',
                'examples': {
                    'application/json': {
                        "success": False,
                        "data": None,
                        "message": "Invalid filter keys or values: title_contains, sal_code",
                        "status": 400
                    }
                }
            }
        }
    )
    def get(self):
        try:
            query_params = request.args.to_dict()
            success, data, message, status = job_service.get_applications_list(query_params)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@job.route('/<string:poster_id>', methods=['GET'], endpoint='job_application')
class Application(Resource):
    """
    특정 채용 공고 관련 API
    """
    @job.doc(
        description="특정 채용 공고를 조회합니다.",
        params={
            'poster_id': '채용 공고 ID'
        },
        responses={
            HTTPStatus.OK.value: {
                'description': '성공적인 응답',
                'examples': {
                    'application/json': {
                        "success": True,
                        "data": {
                            "poster_id": 1,
                            "title": "Python Developer",
                            "comp_id": 123,
                            "salary_code": 3,
                            "edu_code": 2,
                            "deadline": "2024-12-31",
                            "loc_code": [1, 2],
                            "job_code": [101],
                            "view_cnts": 26
                        },
                        "message": "채용 공고를 성공적으로 조회했습니다.",
                        "status": 200
                    }
                }
            },
            HTTPStatus.NOT_FOUND.value: {
                'description': '채용 공고를 찾을 수 없음',
                'examples': {
                    'application/json': {
                        "success": False,
                        "data": None,
                        "message": "채용 공고를 찾을 수 없습니다.",
                        "status": 404
                    }
                }
            }
        }
    )
    def get(self, poster_id):
        try:
            query_params = request.args.to_dict()
            success, data, message, status = job_service.get_application(query_params, poster_id)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
