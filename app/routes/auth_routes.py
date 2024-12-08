from flask import Blueprint
from app.controllers.auth_controller import AuthController
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Register a new user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
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
        201: {
            'description': 'User registered successfully'
        },
        400: {
            'description': 'Bad request'
        }
    }
})
def register():
    return AuthController.register()

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Login user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
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
        200: {
            'description': 'Login successful'
        },
        401: {
            'description': 'Invalid credentials'
        }
    }
})
def login():
    return AuthController.login()

@auth_bp.route('/refresh', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Refresh access token',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Refresh token'
        }
    ],
    'responses': {
        200: {
            'description': 'New access token'
        },
        401: {
            'description': 'Invalid refresh token'
        }
    }
})
def refresh():
    return AuthController.refresh()

@auth_bp.route('/profile', methods=['PUT'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Update user profile',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Access token'
        },
        {
            'name': 'body',
            'in': 'body',
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
        200: {
            'description': 'Profile updated successfully'
        },
        400: {
            'description': 'Bad request'
        },
        401: {
            'description': 'Unauthorized'
        }
    }
})
def update_profile():
    return AuthController.update_profile()