# routes/application_route.py
from flask import request
from flask_restx import Namespace, Resource
from app.services import application_service
from app.views.response import JsonResponse, success, fail  # JsonResponse import
from http import HTTPStatus # HTTP 상태 코드 사용을 위함.

application = Namespace('auth', description='Application related operations')

@application.route('/')
class Application(Resource):
    def post(self):
        try:
            data, message = application_service.applicate(request.json)
            return JsonResponse(data, message).to_response() # JsonResponse로 응답 생성
        except Exception as e: #예외 발생시 fail response 생성
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

    def get(self):
        data, message = application_service.get_application_log(request.args.to_dict())
        return JsonResponse(data, message).to_response() # JsonResponse로 응답 생성

@application.route('/<int:application_id>')
class ApplicationCancel(Resource):
    def delete(self, application_id):
        data, message = application_service.update_application_status(request.json, application_id)
        return JsonResponse(data, message).to_response() # JsonResponse로 응답 생성