from app.utils import responses


def test_auth(data):
    return responses.test_response(201, "Access successfully")