from ..models.database import get_db
from ..models.sal_code import *
from ..models.edu_code import *
from ..models.job_code import *
from ..models.loc_code import *


def get_salary_table(data):
    db = next(get_db())
    page = int(data.get("page", "1"))
    _data = {}
    try:
        result = get_sal_codes(db, page)
        if result['success']:
            _data = result['data']
            return True, _data, "Salary 테이블 조회에 성공했습니다.", 200
        else:
            return False, {}, result["message"], 400
    except Exception as e:
        return False, {}, str(e), 500


def get_education_table(data):
    db = next(get_db())
    page = int(data.get("page", "1"))
    _data = {}
    try:
        result = get_edu_codes(db, page)
        if result['success']:
            _data = result['data']
            return True, _data, "Education 테이블 조회에 성공했습니다.", 200
        else:
            return False, {}, result["message"], 400
    except Exception as e:
        return False, {}, str(e), 500

def get_job_table(data):
    db = next(get_db())
    page = int(data.get("page", "1"))
    _data = {}
    try:
        result = get_job_codes(db, page)
        if result['success']:
            _data = result['data']
            return True, _data, "job 테이블 조회에 성공했습니다.", 200
        else:
            return False, {}, result["message"], 400
    except Exception as e:
        return False, {}, str(e), 500
    
def get_job_name(job_id):
    db = next(get_db())
    
    _data = {}
    try:
        result = get_job_code_by_id(db, job_id)
        if result['success']:
            _data = result['job_code']
            return True, _data, "job name 조회에 성공했습니다.", 200
        else:
            return False, {}, result["message"], 400
    except Exception as e:
        return False, {}, str(e), 500

def get_location_table(data):
    db = next(get_db())
    page = int(data.get("page", "1"))
    _data = {}
    try:
        result = get_loc_codes(db, page)
        if result['success']:
            _data = result['data']
            return True, _data, "조회에 성공했습니다.", 200
        else:
            return False, {}, result["message"], 400
    except Exception as e:
        return False, {}, str(e), 500
    

def get_loc_data(loc_code):
    db = next(get_db())
    
    _data = {}
    try:
        result = get_loc_code_by_id(db, loc_code)
        if result['success']:
            _data = result['loc_code']
            return True, _data, "loc data 조회에 성공했습니다.", 200
        else:
            return False, {}, result["message"], 400
    except Exception as e:
        return False, {}, str(e), 500