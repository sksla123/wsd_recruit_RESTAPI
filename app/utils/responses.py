from flask import jsonify

def test_response(status_code, message):
    response = jsonify({
        'status': 'success',
        'message': message
    })
    response.status_code = status_code
    return response















# def success_response(status_code, message):
#     """Returns a success response with a message."""
#     response = jsonify({
#         'status': 'success',
#         'message': message
#     })
#     response.status_code = status_code
#     return response

# def error_response(status_code, message):
#     """Returns an error response with a message."""
#     response = jsonify({
#         'status': 'error',
#         'message': message
#     })
#     response.status_code = status_code
#     return response

# def token_response(status_code, message, access_token, refresh_token):
#     """Returns a success response with tokens."""
#     response = jsonify({
#         'status': 'success',
#         'message': message,
#         'access_token': access_token,
#         'refresh_token': refresh_token
#     })
#     response.status_code = status_code
#     return response

# # Response models for Swagger documentation
# response_model = {
#     'status': 'success',
#     'message': 'Operation successful'
# }

# error_model = {
#     'status': 'error',
#     'message': 'Error message'
# }

# token_model = {
#     'status': 'success',
#     'message': 'Login successful',
#     'access_token': 'JWT access token',
#     'refresh_token': 'JWT refresh token'
# }