import re
from email_validator import validate_email, EmailNotValidError

def validate_email_format(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_password_strength(password):
    # 최소 8자, 대문자, 소문자, 숫자, 특수문자 포함
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password) is not None