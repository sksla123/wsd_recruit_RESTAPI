# routes/job_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import job_service
from app.views.response import JsonResponse, fail
from http import HTTPStatus

job = Namespace('job', description='poster related operations')

# Query parameters 모델 정의 (Swagger 문서화)
job_filters = job.model('JobFilters', {
   
})

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
            HTTPStatus.OK.value: '성공적인 응답',
            HTTPStatus.BAD_REQUEST.value: '잘못된 요청',
        }
    )
    def get(self):
        """
        채용 공고 목록을 조회합니다.

        쿼리 파라미터를 사용하여 

        Returns:
            flask.Response: JSON 응답
        """
        try:
            query_params = request.args.to_dict()  # 쿼리 파라미터를 딕셔너리로 받음
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
            HTTPStatus.OK.value: '성공적인 응답',
            HTTPStatus.NOT_FOUND.value: '채용 공고를 찾을 수 없음',
        }
    )
    def get(self, poster_id):
        """
        특정 채용 공고를 조회합니다.

        Args:
            poster_id (int): 조회할 채용 공고 ID

        Returns:
            flask.Response: JSON 응답
        """
        try:
            query_params = request.args.to_dict()  # 필요하면 query_params 사용
            success, data, message, status = job_service.get_application(query_params, poster_id)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)