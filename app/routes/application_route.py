from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import application_service
from app.views.response import JsonResponse, fail
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

application = Namespace('application', description='Application related operations')

parser = application.parser()
parser.add_argument('page', type=int, help='페이지 번호 (기본값: 1)', location='args', default=1)

# 모델 정의
application_add_model = application.model('ApplicationAdd', {
    'poster_id': fields.String(required=True, description='포스터 아이디', example='rec-49562675'),
    "application": fields.String(required=True, description='지원서류 내용', example="I am interested in this job position and believe my skills match the requirements."),
})

application_update_model = application.model('ApplicationUpdate', {
    'application_id': fields.Integer(required=True, description='지원 서류 아이디', example=1),
    "action": fields.String(required=True, description='수정할 종류\n가능한 Action = ["application", # 추후 확장성을 위해 여러개 가능하게 만듦]', example="application"),
    "new_value": fields.String(required=True, description='지원서류 내용(Action=="application")/그 외 기능[미구현](Action=="?")', example="I'm really eager to work.")
})

application_cancel_model = application.model('ApplicationCancel', {
    'application_id': fields.Integer(description='Application ID', example='1'),
})

@application.route('/')
class Application(Resource):
    @application.expect(application_add_model)
    @application.doc(responses={
        200: '''{
  "status": "success",
  "message": "Application submitted successfully",
  "data": {
    "application_id": 2,
    "user_id": "example_user",
    "poster_id": "rec-49562675",
    "application": "I am interested in this job position and believe my skills match the requirements.",
    "application_status": 0
  }
}''',
        400: '''{
  "status": "failed",
  "message": "Failed to submit application"
}'''
    })
    @jwt_required()
    def post(self):
        """
        지원 신청을 처리합니다.
        """
        current_user = get_jwt_identity()
        try:
            success, data, message, status = application_service.applicate(request.json, current_user)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))
    
    @application.doc(
        description="지원 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''{
  "status": "success",
  "message": "Application list is loaded successfully",
  "data": {
    "user_applicateds": [
      {
        "application_id": 2,
        "user_id": "example_user",
        "poster_id": "rec-49562675",
        "application": "I am interested in this job position and believe my skills match the requirements.",
        "application_status": 0
      }
    ],
    "total_count": 1,
    "current_page": 1,
    "total_page": 1
  }
}''',
        }
    )
    @jwt_required()
    def get(self):
        """
        사용자가 제출한 지원서를 조회합니다.
        """
        current_user = get_jwt_identity()
        success, data, message, status = application_service.get_user_applications(request.args.to_dict(), current_user)
        return JsonResponse(success, data, message, status).to_response()

    @application.expect(application_update_model)
    @application.doc(responses={
        200: '''
{
  "status": "success",
  "message": "Application updated successfully",
  "data": {
    "application_id": 2,
    "user_id": "example_user",
    "poster_id": "rec-49562675",
    "application": "I'm really eager to work.",
    "application_status": 0
  }
}''',
        400: '''{
  "status": "failed",
  "message": "지원서를 찾을 수 없습니다."
}''',
    })
    @jwt_required()
    def put(self):
        """
        지원 신청 내용을 업데이트 합니다.
        """
        current_user = get_jwt_identity()
        try:
            success, data, message, status = application_service.update_application(request.json, current_user)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e))

@application.route('/<int:application_id>')
@application.param('application_id', '지원 서류 ID', example='1')
class ApplicationCancel(Resource):
    @application.doc(
        responses={
        200: '''{
  "status": "success",
  "message": "Application canceled successfully",
  "data": {
    "application_id": 2,
    "user_id": "example_user",
    "poster_id": "rec-49562675",
    "application": "I am interested in this job position and believe my skills match the requirements.",
    "application_status": 0
  }
}''',
        404: '''{
  "status": "failed",
  "message": "Application not found"
}'''
    })
    @jwt_required()
    def delete(self, application_id):
        """
        지원을 취소합니다.
        """
        current_user = get_jwt_identity()
        success, data, message, status = application_service.cancel_application_status(application_id, current_user)
        return JsonResponse(success, data, message, status).to_response()

@application.route('/logs')
class ApplicationLog(Resource):
    @application.doc(
        description="지원서 관련 로그를 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''{
  "status": "success",
  "message": "Application logs retrieved successfully",
  "data": {
    "user_applicated_log": [
      {
        "application_log_id": 1,
        "application_id": 1,
        "applicated_at": "2024-12-18T17:47:34",
        "user_id": "example_user",
        "poster_id": "rec-49562675",
        "applicate_action": 0
      },
      {
        "application_log_id": 2,
        "application_id": 1,
        "applicated_at": "2024-12-18T17:47:51",
        "user_id": "example_user",
        "poster_id": "rec-49562675",
        "applicate_action": 2
      }
    ],
    "total_count": 2,
    "current_page": 1,
    "total_page": 1
  }
}''',
        }
    )
    @jwt_required()
    def get(self):
        """
        지원 로그를 조회합니다.
        """
        current_user = get_jwt_identity()
        success, data, message, status = application_service.get_application_log(request.args.to_dict(), current_user)
        return JsonResponse(success, data, message, status).to_response()