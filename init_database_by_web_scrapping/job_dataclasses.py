import pandas as pd
from dataclasses import dataclass, field

@dataclass
class JobCodeTable():
    '''
    plan_strategy: 기획·전략
    marketing: 마케팅·홍보·조사
    accounting: 회계·세무·재무
    hrd: 인사·노무·HRD
    management: 총무·법무·사무
    it: IT개발·데이터
    design: 디자인
    business: 영업·판매·무역
    tm: 고객상담·TM
    distribution: 구매·자재·물류
    md: 상품기획·MD
    transit: 운전·운송·배송
    service: 서비스
    production: 생산
    building: 건설·건축
    medic: 의료
    research: 연구·R&D
    edu: 교육
    culture: 미디어·문화·스포츠
    finance: 금융·보험
    public: 공공·복지

    toKoreanDict를 통해 각 변수의 한국어 명을 확인 가능
    '''
    plan_strategy: pd.DataFrame
    marketing: pd.DataFrame
    accounting: pd.DataFrame
    hrd: pd.DataFrame
    management: pd.DataFrame
    it: pd.DataFrame
    design: pd.DataFrame
    business: pd.DataFrame
    tm: pd.DataFrame
    distribution: pd.DataFrame
    md: pd.DataFrame
    transit: pd.DataFrame
    service: pd.DataFrame
    production: pd.DataFrame
    building: pd.DataFrame
    medic: pd.DataFrame
    research: pd.DataFrame
    edu: pd.DataFrame
    culture: pd.DataFrame
    finance: pd.DataFrame
    public: pd.DataFrame

    toKoreanDict: dict = field(init=False)

    def __post_init__(self):
        self.toKoreanDict = {
            'plan_strategy': '기획·전략',
            'marketing': '마케팅·홍보·조사',
            'accounting': '회계·세무·재무',
            'hrd': '인사·노무·HRD',
            'management': '총무·법무·사무',
            'it': 'IT개발·데이터',
            'design': '디자인',
            'business': '영업·판매·무역',
            'tm': '고객상담·TM',
            'distribution': '구매·자재·물류',
            'md': '상품기획·MD',
            'transit': '운전·운송·배송',
            'service': '서비스',
            'production': '생산',
            'building': '건설·건축',
            'medic': '의료',
            'research': '연구·R&D',
            'edu': '교육',
            'culture': '미디어·문화·스포츠',
            'finance': '금융·보험',
            'public': '공공·복지',
        }

    def get_total_dataframe(self):
        dfs = [getattr(self, field) for field in self.toKoreanDict.keys()]  # 각 DataFrame을 리스트로 가져오기
        total_df = pd.concat(dfs, ignore_index=True)  # 모든 DataFrame을 합침, index는 다시 재설정
        return total_df    

@dataclass
class CodeTable():
    '''
    'job_type': '근무형태 코드',
    'edu': '학력 코드',
    'sal': '연봉 범위 코드',
    'total_loc': '사람인 근무지/지역 코드',
    'loc_2': '2차 근무지/지역 코드',
    'loc_1': '1차 근무지/지역 코드',
    'ind_1': '상위 산업/업종 코드',
    'ind_2': '산업/업종 코드',
    'ind_3': '업종 키워드 코드',
    'job': '직무 테이블',
    'jobCodeTable': '세부 직무 직업 테이블',

    toKoreanDict를 통해 각 변수의 한국어 명을 확인 가능

    '''
    job_type: pd.DataFrame
    edu: pd.DataFrame
    sal: pd.DataFrame
    total_loc: pd.DataFrame
    loc_2: pd.DataFrame
    loc_1: pd.DataFrame
    ind_1: pd.DataFrame
    ind_2: pd.DataFrame
    ind_3: pd.DataFrame
    job: pd.DataFrame
    jobCodeTable: JobCodeTable

    toKoreanDict: dict = field(init=False)

    def __post_init__(self):
        self.toKoreanDict = {
            'job_type': '근무형태 코드',
            'edu': '학력 코드',
            'sal': '연봉 범위 코드',
            'total_loc': '사람인 근무지/지역 코드',
            'loc_2': '2차 근무지/지역 코드',
            'loc_1': '1차 근무지/지역 코드',
            'ind_1': '상위 산업/업종 코드',
            'ind_2': '산업/업종 코드',
            'ind_3': '업종 키워드 코드',
            'job': '직무 테이블',
            'jobCodeTable': '세부 직무 직업 테이블',
        }