# routes/job_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import job_service
from app.views.response import JsonResponse, fail # JsonResponse, success, fail import
from http import HTTPStatus

job = Namespace('job', description='poster related operations')

@job.route('/')
class Applications(Resource):
    """
    채용 공고 목록 관련 API
    """
    def get(self):
        """
        채용 공고 목록을 조회합니다.

        쿼리 파라미터를 사용하여 필터링할 수 있습니다.

        Returns:
            flask.Response: JSON 응답
        """
        try:
            query_params = request.args.to_dict()
            success, data, message, status = job_service.get_applications_list(query_params)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@job.route('/<int:poster_id>')
class Application(Resource):
    """
    특정 채용 공고 관련 API
    """
    def get(self, poster_id):
        """
        특정 채용 공고를 조회합니다.

        Args:
            poster_id (int): 조회할 채용 공고 ID

        Returns:
            flask.Response: JSON 응답
        """
        try:
            query_params = request.args.to_dict() # 필요하면 query_params 사용
            success, data, message, status = job_service.get_application(query_params, poster_id)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)