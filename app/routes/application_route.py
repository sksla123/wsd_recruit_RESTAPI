from flask import request
from flask_restx import Namespace, Resource, fields
from services import application_service

application = Namespace('auth', description='Application related operations')

@application.route('/')
class Application(Resource):
    def post(self):

        return application_service.applicate(request.json)
    
    def get(self):
        
        query_params = request.args.to_dict()
        return application_service.get_application_log(query_params)
    

@application.route('/<int:application_id>')
class ApplicationCancel(Resource):
    def delete(self, application_id):

        return application_service.update_application_status(request.json, application_id)