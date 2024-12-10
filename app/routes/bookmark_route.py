from flask import request
from flask_restx import Namespace, Resource, fields
from services import bookmark_service

bookmark = Namespace('bookmark', description='User Bookmark related operations')

@bookmark.route('/register')
class Bookmarks(Resource):
    def post(self):
        
        return bookmark_service.register_user(request.json)
    
    def get(self):
        
        query_params = request.args.to_dict()
        return bookmark_service.get_application_log(query_params)
    
