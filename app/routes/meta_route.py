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
    @jwt_required()
    @meta.doc(
        description="메타 테이블 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''''',
        }
    )
    def get(self):
        """
        메타 테이블블 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        current_user = get_jwt_identity()

        try:
            success, data, message, status =  meta_service.get_bookmarks(request.args.to_dict(), current_user)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@meta.route('/edu')
class GetSalaryTable(Resource):
    @jwt_required()
    @meta.doc(
        description="메타 테이블블 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''''',
        }
    )
    def get(self):
        """
        메타 테이블블 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        current_user = get_jwt_identity()

        try:
            success, data, message, status =  meta_service.get_bookmarks(request.args.to_dict(), current_user)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
        
