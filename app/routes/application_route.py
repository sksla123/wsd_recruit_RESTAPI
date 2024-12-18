from flask import request
from flask_restx import Namespace, Resource
from app.services import application_service
from app.views.response import JsonResponse, fail
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

application = Namespace('application', description='Application related operations')

@application.route('/')
class Application(Resource):
    """
    지원 관련 API를 제공합니다.
    """
    def post(self):
        """
        지원 신청을 처리합니다.

        요청 본문에 지원 데이터를 JSON 형식으로 포함해야 합니다.

        Returns:
            JsonResponse: 지원 신청 결과 데이터와 메시지
        """
        try:
            success, data, message, status = application_service.applicate(request.json)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))
    
    @jwt_required()
    def get(self):
        """
        지원 로그를 조회합니다.

        쿼리 파라미터로 필터링 조건을 지정할 수 있습니다.

        Returns:
            JsonResponse: 지원 로그 데이터와 메시지
        """
        
        current_user = get_jwt_identity()
        # print(current_user)
        
        success, data, message, status = application_service.get_application_log(request.args.to_dict(), current_user)
        return JsonResponse(success, data, message, status).to_response()

@application.route('/<int:application_id>')
class ApplicationCancel(Resource):
    """
    지원 취소 관련 API를 제공합니다.
    """
    def delete(self, application_id):
        """
        지원을 취소합니다.

        Path variable로 지원 아이디를 전달해야 합니다.

        Returns:
            JsonResponse: 지원 취소 결과 데이터와 메시지
        """
        success, data, message, status = application_service.update_application_status(request.json, application_id)
        return JsonResponse(success, data, message, status).to_response()
