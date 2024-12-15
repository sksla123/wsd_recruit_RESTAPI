# routes/bookmark_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import bookmark_service
from app.views.response import JsonResponse, fail # JsonResponse, success, fail import
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

bookmark = Namespace('bookmark', description='User Bookmark related operations')

@bookmark.route('/register')
class Bookmarks(Resource):
    """
    북마크 관련 API를 제공합니다.
    """
    @jwt_required()
    def post(self):
        """
        북마크를 등록합니다.

        요청 본문에 북마크 정보를 JSON 형식으로 포함해야 합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        try:
            user_id = get_jwt_identity()

            success, data, message, status = bookmark_service.register_bookmark(request.json, user_id)
            return JsonResponse(success, data, message, status ).to_response() # 201 Created
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@bookmark.route('/')
class GetBookmarks(Resource):
    @jwt_required()
    def get(self):
        """
        북마크 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        current_user = get_jwt_identity()

        try:
            success, data, message, status =  bookmark_service.get_bookmarks(current_user)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)