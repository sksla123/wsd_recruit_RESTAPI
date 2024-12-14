# routes/bookmark_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import bookmark_service

bookmark = Namespace('bookmark', description='User Bookmark related operations')

@bookmark.route('/register')
class Bookmarks(Resource):
    def post(self):
        
        return bookmark_service.register_user(request.json)
    
    def get(self):
        
        return bookmark_service.get_application_log(request.json)
    
