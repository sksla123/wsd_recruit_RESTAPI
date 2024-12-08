from flask import Blueprint
from app.controllers.auth_controller import AuthController
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_controller = AuthController()

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': '회원가입',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '201': {'description': '회원가입 성공'},
        '400': {'description': '잘못된 입력'},
        '409': {'description': '이미 존재하는 사용자'}
    }
})
def register():
    return auth_controller.register()

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': '로그인',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '200': {'description': '로그인 성공'},
        '401': {'description': '인증 실패'}
    }
})
def login():
    return auth_controller.login()