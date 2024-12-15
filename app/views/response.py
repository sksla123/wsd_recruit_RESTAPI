# views/response.py
class JsonResponse:
    def __init__(self, success, data=None, message=None, status_code=200):
        self.success = success
        self.data = data
        self.message = message
        self.status_code = status_code

    def to_dict(self):  # JSON으로 변환할 딕셔너리 생성
        response_dict = {'status': "success"}
        if not self.success:
            response_dict['status'] = "failed"
        if self.message is not None:
            response_dict['message'] = self.message
        if self.data is not None:  # data가 있을 때만 추가
            response_dict["data"] = self.data

        return response_dict

    def to_response(self):
        return self.to_dict(), self.status_code # 딕셔너리와 status_code를 함께 반환

# 알 수 없는 에러 처리
def fail(message="실패", status_code=500):
    return {
        "status": "failed",
        "message": message
    }, status_code 