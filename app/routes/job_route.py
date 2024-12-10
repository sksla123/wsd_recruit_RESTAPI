from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import job_service

job = Namespace('job', description='poster related operations')

@job.route('/')
class Applications(Resource):    
    def get(self):
        
        query_params = request.args.to_dict()
        return job_service.get_applications_list(query_params)
    
@job.route('/<int:poster_id>')
class Application(Resource):
    def get(self, poster_id):
        query_params = request.args.to_dict()
        return job_service.get_application(query_params)