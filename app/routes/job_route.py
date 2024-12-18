# routes/job_route.py
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import job_service
from app.views.response import JsonResponse, fail
from http import HTTPStatus

job = Namespace('job', description='poster related operations')

# Query parameters 모델 정의 (Swagger 문서화)
job_filters = job.model('JobFilters', {
    'page': fields.Integer(example=1, description="페이지 번호 (기본값: 1)"),
    'sort_by': fields.String(example="deadline_date", description="정렬 기준 (기본값: deadline_date)\n가능한 값: ['deadline_date', 'last_updated_date', 'edu_code', 'sal_code', 'poster_title']"),
    'sort_order': fields.String(example="asc", description="정렬 순서 (asc 또는 desc)"),
    'title_contains': fields.String(example="정규직", description="제목을 포함한 검색어"),
    'comp_id': fields.Integer(example=101, description="회사의 ID"),
    'sal_code_eq': fields.Integer(example=3, description="급여 코드 필터 (equals)"),
    'sal_code_gte': fields.Integer(example=2, description="급여 코드 필터 (greater than or equal to)"),
    'sal_code_lte': fields.Integer(example=5, description="급여 코드 필터 (less than or equal to)"),
    'edu_code_eq': fields.Integer(example=1, description="학력 코드 필터 (equals)"),
    'edu_code_gte': fields.Integer(example=2, description="학력 코드 필터 (greater than or equal to)"),
    'edu_code_lte': fields.Integer(example=3, description="학력 코드 필터 (less than or equal to)"),
    'deadline_date_eq': fields.String(example="2024-12-31", description="마감일 필터 (equals)"),
    'deadline_date_gte': fields.String(example="2024-12-29", description="마감일 필터 (greater than or equal to)"),
    'deadline_date_lte': fields.String(example="2024-12-28", description="마감일 필터 (less than or equal to)"),
    'loc_codes': fields.List(fields.Integer, example=[101000], description="위치 코드 필터 (리스트)"),
    'job_codes': fields.List(fields.Integer, example=[2225], description="직업 코드 필터 (리스트)")
})

parser = job.parser()
parser.add_argument('page', type=int, help='페이지 번호 (기본값: 1)', location='args', default=1)
parser.add_argument('sort_by', type=str, help='정렬 기준 (기본값: deadline_date)', location='args', default='deadline_date', choices=['deadline_date', 'last_updated_date', 'edu_code', 'sal_code', 'poster_title'])
parser.add_argument('sort_order', type=str, help='정렬 순서 (asc 또는 desc)', location='args', default='asc', choices=['asc', 'desc'])
parser.add_argument('title_contains', type=str, help='제목을 포함한 검색어', location='args')
parser.add_argument('comp_id', type=int, help='회사의 ID', location='args')
parser.add_argument('sal_code_eq', type=int, help='급여 코드 필터 (equals)', location='args')
parser.add_argument('sal_code_gte', type=int, help='급여 코드 필터 (greater than or equal to)', location='args')
parser.add_argument('sal_code_lte', type=int, help='급여 코드 필터 (less than or equal to)', location='args')
parser.add_argument('edu_code_eq', type=int, help='학력 코드 필터 (equals)', location='args')
parser.add_argument('edu_code_gte', type=int, help='학력 코드 필터 (greater than or equal to)', location='args')
parser.add_argument('edu_code_lte', type=int, help='학력 코드 필터 (less than or equal to)', location='args')
parser.add_argument('deadline_date_eq', type=str, help='마감일 필터 (equals)', location='args')
parser.add_argument('deadline_date_gte', type=str, help='마감일 필터 (greater than or equal to)', location='args')
parser.add_argument('deadline_date_lte', type=str, help='마감일 필터 (less than or equal to)', location='args')
parser.add_argument('loc_codes', type=int, help='위치 코드 필터 (리스트)', location='args', action='append')
parser.add_argument('job_codes', type=int, help='직업 코드 필터 (리스트)', location='args', action='append')

@job.route('/')
class Applications(Resource):
    """
    채용 공고 목록 관련 API
    """
    @job.doc(
        security=None,
        description="채용 공고 목록을 조회합니다.",
        params={
            'page': '페이지 번호 (기본값: 1)',
            'sort_by': "정렬 기준 (기본값: deadline_date)\n가능한 값(이 중 하나만 가능): ['deadline_date', 'last_updated_date', 'edu_code', 'sal_code', 'poster_title']",
            'sort_order': '정렬 순서 (asc 또는 desc)',
            'title_contains': '제목을 포함한 검색어',
            'comp_id': '회사의 ID',
            'sal_code_eq': '급여 코드 필터 (equals)',
            'sal_code_gte': '급여 코드 필터 (greater than or equal to)',
            'sal_code_lte': '급여 코드 필터 (less than or equal to)',
            'edu_code_eq': '학력 코드 필터 (equals)',
            'edu_code_gte': '학력 코드 필터 (greater than or equal to)',
            'edu_code_lte': '학력 코드 필터 (less than or equal to)',
            'deadline_date_eq': '마감일 필터 (equals)',
            'deadline_date_gte': '마감일 필터 (greater than or equal to)',
            'deadline_date_lte': '마감일 필터 (less than or equal to)',
            'loc_codes': '위치 코드 필터 (리스트)',
            'job_codes': '직업 코드 필터 (리스트)'
        },
        responses={
            HTTPStatus.OK.value: '''
{
    "status": "success",
    "message": "채용 공고 목록을 성공적으로 조회했습니다.",
    "data": {
        "postings": [
            {
                "comp_id": 13,
                "poster_id": "rec-49244800",
                "poster_title": "[아이디클리닉] 네트워크 마케팅 팀장 채용",
                "deadline_date": "2024-12-20",
                "edu_code": 2,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 217,
                "poster_id": "rec-49286433",
                "poster_title": "[핏펫] 상품기획 담당자(BM)",
                "deadline_date": "2024-12-20",
                "edu_code": 0,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 263,
                "poster_id": "rec-49411965",
                "poster_title": "[안진회계법인] 금융감사 및 자문 그룹(FS) 신용리스크 컨설턴트",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2259"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 118,
                "poster_id": "rec-49434130",
                "poster_title": "[테크빌교육] 연수사업 회계관리 담당자 채용",
                "deadline_date": "2024-12-20",
                "edu_code": 0,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 297,
                "poster_id": "rec-49435037",
                "poster_title": "[음성 AI 기업 덴컴] 전략기획팀 팀장 모집",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2259"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 321,
                "poster_id": "rec-49435341",
                "poster_title": "[동아제약] 경영기획 부문 경력직 채용",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2259",
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 212,
                "poster_id": "rec-49437050",
                "poster_title": "(주) 심리야 경영지원팀 모집합니다",
                "deadline_date": "2024-12-20",
                "edu_code": 0,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 316,
                "poster_id": "rec-49437603",
                "poster_title": "각 부문 관리자채용(재무/영업관리)",
                "deadline_date": "2024-12-20",
                "edu_code": 0,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 203,
                "poster_id": "rec-49437973",
                "poster_title": "경영 컨설턴트 채용 ( IT 전략경영 )",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 276,
                "poster_id": "rec-49438468",
                "poster_title": "디자인토큰(주) 회계/관리/경영지원 경력사원 모집",
                "deadline_date": "2024-12-20",
                "edu_code": 2,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 468,
                "poster_id": "rec-49438487",
                "poster_title": "사업기획, 제안서 작성, 문서작성",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 453,
                "poster_id": "rec-49439051",
                "poster_title": "[뚝섬미술관] 전시 운영, 기획 보조 인력 구인 공고",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 376,
                "poster_id": "rec-49439642",
                "poster_title": "전산업무 사무직 모집합니다. (30분단축근무)(신입채용)",
                "deadline_date": "2024-12-20",
                "edu_code": 0,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 167,
                "poster_id": "rec-49439800",
                "poster_title": "국방사업 프로젝트매니저 채용",
                "deadline_date": "2024-12-20",
                "edu_code": 1,
                "job_codes": [
                    "2259"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 410,
                "poster_id": "rec-49440860",
                "poster_title": "(주)이롬넷 경영기획팀 경력자 모집",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 28,
                "poster_id": "rec-49441006",
                "poster_title": "[기획/ 사무직렬] 서울 명동 컨설팅 펌 직원 모집",
                "deadline_date": "2024-12-20",
                "edu_code": 2,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 6,
                "poster_status": 1
            },
            {
                "comp_id": 407,
                "poster_id": "rec-49446408",
                "poster_title": "[The SMC]  홍보 ·재무회계 · 전략AE ·조직문화 · 인사(인턴)  경영 직군 신입/ 경력 채용",
                "deadline_date": "2024-12-20",
                "edu_code": 0,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 221,
                "poster_id": "rec-49448359",
                "poster_title": "재무회계 담당자 채용",
                "deadline_date": "2024-12-20",
                "edu_code": 2,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000",
                    "101010"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 295,
                "poster_id": "rec-49456163",
                "poster_title": "[한국하니웰] IA Leader (경력 15년 이상)",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            },
            {
                "comp_id": 81,
                "poster_id": "rec-49460815",
                "poster_title": "경영기획 담당자 채용 (신입)",
                "deadline_date": "2024-12-20",
                "edu_code": 3,
                "job_codes": [
                    "2225"
                ],
                "loc_codes": [
                    "101000"
                ],
                "sal_code": 1,
                "poster_status": 1
            }
        ],
        "total_count": 584,
        "current_page": 3,
        "total_page": 30
    }
}
''',
            HTTPStatus.BAD_REQUEST.value: '''
{
    "status": "failed",
    "message": "Not valid sorting option."
}
''',
        }
    )
    @job.expect(parser)
    def get(self):
        """
        채용 공고 목록을 조회합니다.

        쿼리 파라미터를 사용하여 

        Returns:
            flask.Response: JSON 응답
        """
        try:
            query_params = request.args.to_dict()  # 쿼리 파라미터를 딕셔너리로 받음
            success, data, message, status = job_service.get_applications_list(query_params)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

@job.route('/<string:poster_id>', methods=['GET'], endpoint='job_application')
@job.param('poster_id', '채용 공고 ID', example='rec-49526533')
class Application(Resource):
    """
    특정 채용 공고 관련 API
    """
    @job.doc(
        security=None,
        description="특정 채용 공고를 조회합니다.",
        responses={
            HTTPStatus.OK.value: '''
{
  "status": "success",
  "message": "채용 공고를 성공적으로 조회했습니다.",
  "data": {
    "comp_id": 40,
    "poster_id": "rec-49526533",
    "poster_title": "[ 메가스터디그룹 ] 메가엠디(주) 사업지원실 정규직 채용",
    "poster_link": "https://www.saramin.co.kr/zf_user/jobs/relay/view?view_type=list&rec_idx=49526533",
    "job_sectors": "[\"DW\", \"SQL\", \"Excel\", \"PowerPoint\", \"경영지원\"]",
    "job_career": "경력무관 · 정규직",
    "job_education": "대학교(4년)↑",
    "edu_code": 3,
    "edu_upper": 1,
    "deadline_date": "2024-12-22",
    "last_updated_date": "2024-12-05",
    "job_codes": [
      "2225"
    ],
    "loc_codes": [
      "101000"
    ],
    "sal_code": 1,
    "poster_status": 1,
    "poster_writer_user_id": "admin",
    "view_cnts": 1
  }
}
''',
            HTTPStatus.NOT_FOUND.value: '''
{
  "status": "failed",
  "message": "JobPosting을 찾을 수 없습니다."
}
''',
        }
    )
    def get(self, poster_id):
        """
        특정 채용 공고를 조회합니다.

        Args:
            poster_id (int): 조회할 채용 공고 ID

        Returns:
            flask.Response: JSON 응답
        """
        try:
            query_params = request.args.to_dict()  # 필요하면 query_params 사용
            success, data, message, status = job_service.get_application(query_params, poster_id)
            return JsonResponse(success, data, message, status).to_response()
        except Exception as e:
            return fail(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)