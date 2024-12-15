# utils/util.py
import re

import base64

from datetime import datetime
from zoneinfo import ZoneInfo

def now_korea():
    return datetime.now(ZoneInfo("Asia/Seoul"))

def base64_encode(s):
    """
    주어진 문자열을 base64로 인코딩합니다.
    
    Args:
    s: 인코딩할 문자열.
    
    Returns:
    base64로 인코딩된 문자열.
    """
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')


def base64_decode(s):
    """
    주어진 base64 문자열을 디코딩합니다.
    
    Args:
    s: 디코딩할 base64 문자열.
    
    Returns:
    디코딩된 문자열.
    """
    return base64.b64decode(s.encode('utf-8')).decode('utf-8')

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

from datetime import datetime, timezone

def calculate_remaining_time(token_dict):
    exp_timestamp = token_dict.get('exp')
    if exp_timestamp is None:
        return "토큰에서 만료 시간을 찾을 수 없습니다"
    current_time = datetime.now(timezone.utc).timestamp()
    remaining_time = exp_timestamp - current_time
    return max(remaining_time, 0)  # 음수 값 방지