# routes/bookmark_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import bookmark_service
from app.views.response import JsonResponse, fail # JsonResponse, success, fail import
from http import HTTPStatus

bookmark = Namespace('bookmark', description='User Bookmark related operations')

@bookmark.route('/register')
class Bookmarks(Resource):
    """
    북마크 관련 API를 제공합니다.
    """
    def post(self):
        """
        북마크를 등록합니다.

        요청 본문에 북마크 정보를 JSON 형식으로 포함해야 합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        try:
            data, message = bookmark_service.register_bookmark(request.json)
            return JsonResponse(data, message, HTTPStatus.CREATED).to_response() # 201 Created
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


    def get(self):
        """
        북마크 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        try:
            data, message = bookmark_service.get_bookmarks(request.args.to_dict())
            return JsonResponse(data, message).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)