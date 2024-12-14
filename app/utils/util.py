import base64

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