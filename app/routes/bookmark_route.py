# routes/bookmark_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import bookmark_service
from app.views.response import JsonResponse, fail # JsonResponse, success, fail import
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

bookmark = Namespace('bookmark', description='User Bookmark related operations')


parser = bookmark.parser()
parser.add_argument('page', type=int, help='페이지 번호 (기본값: 1)', location='args', default=1)

@bookmark.route('/')
class GetBookmarks(Resource):
    @jwt_required()
    @bookmark.doc(
        description="북마크 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
        },
        responses={
            HTTPStatus.OK.value: '''''',
        }
    )
    def get(self):
        """
        북마크 목록을 조회합니다.

        Returns:
            flask.Response: JSON 형태의 응답
        """
        current_user = get_jwt_identity()

        try:
            success, data, message, status =  bookmark_service.get_bookmarks(request.args.to_dict(), current_user)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
        
@bookmark.route('/<string:poster_id>')
@bookmark.param('poster_id', '지원 서류 ID', example='rec-49562675')
class ApplicationCancel(Resource):
    @bookmark.doc(
        responses={
        200: '''''',
        404: ''''''
    })
    @jwt_required()
    def post(self, poster_id):
        """
        지원을 취소합니다.
        """
        current_user = get_jwt_identity()
        success, data, message, status = bookmark_service.toggle_bookmark(current_user, poster_id)
        return JsonResponse(success, data, message, status).to_response()