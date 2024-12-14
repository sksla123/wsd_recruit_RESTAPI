# views/response.py
from flask import jsonify

class JsonResponse:
    def __init__(self, data=None, message="", status_code=200):
        self.data = data
        self.message = message
        self.status_code = status_code

    def to_dict(self):  # JSON으로 변환할 딕셔너리 생성
        response_dict = {
            "message": self.message
        }
        if self.data is not None:  # data가 있을 때만 추가
            response_dict["data"] = self.data
        return response_dict

    def to_response(self):
        return jsonify(self.to_dict()), self.status_code # jsonify와 status_code를 함께 반환

# 기존의 success, fail 함수도 유지 가능. 상황에 따라 선택적으로 사용
def success(data=None, message="성공"):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), 200

def fail(message="실패", status_code=400):
    return jsonify({
        "status": "fail",
        "message": message
    }), status_code
