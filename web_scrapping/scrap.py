import os
import time
import urllib.parse
import pandas as pd

from tqdm.auto import tqdm

import requests
from bs4 import BeautifulSoup

from dataclasses import dataclass, field

import gzip

def getResponsedHtml(url, 
                     headers = {
                            # Robots.txt 방지용
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                         }, 
                     num_of_tries=5, 
                     cache_folder='./__htmlCache__',
                     ignore_cache=False,
                     ):
    '''
    반복된 요청으로 차단되지 않도록, cache 폴더에 html을 백업해두고 필요시 url로 요청하지 않고 폴더에서 꺼내옴
    만약 오래된 cache 파일을 무시하게 하고 싶으면, ignore_cache 플래그를 True로 설정
    '''
    
    safe_file_name = urllib.parse.quote(url, safe='')
    cache_file_path = os.path.join(cache_folder, f'{safe_file_name}.txt.gz')

    os.makedirs(cache_folder, exist_ok=True)

    if (not ignore_cache and os.path.exists(cache_file_path)):
        with gzip.open(cache_file_path, 'rt', encoding='utf-8') as f:
            html = BeautifulSoup(f.read(), 'html.parser')
        # print('cache에서 불러옴')
        return html
    else:
        while(num_of_tries != 0):
            response = requests.get(url, headers=headers, timeout=20)
            if(response.status_code != 200):
                print(response.status_code, "failed")
                num_of_tries -= 1
                time.sleep(3) # 임시 차단되었을 가능성이 있으므로 3초 쉬고 재시도
                continue
            html = BeautifulSoup(response.text, 'html.parser')
            with gzip.open(cache_file_path, 'wt', encoding='utf-8') as f:
                f.write(str(html))
                # print('cache 저장됨')
            return html
    
    return None

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

class WebScarpperBase():
    def  __init__(self, base_url, headers, num_of_tries=5, cache_folder='./__htmlCache__'):
        self.base_url = base_url
        self.headers = headers
        self.num_of_tries = num_of_tries
        self.cache_folder = cache_folder
        self.ignore_cache = False
        
        self.urls={}

    def setIgnoreCache(self, flag=False):
        self.ignore_cache = flag
        
class WebScrapperCodeTable(WebScarpperBase):
    def  __init__(self, base_url, headers, num_of_tries=5, cache_folder='./__htmlCache__'):
        super().__init__(base_url, headers, num_of_tries, cache_folder)
        
        # 근무형태/학력/연봉 코드용 url
        self.urls['extra_code'] = self.base_url + "/guide/code-table1"
        # 근무지/지역 코드용 url
        self.urls['loc_code'] = self.base_url + "/guide/code-table2"
        # 산업/업종 코드용 url
        self.urls['industry_code'] = self.base_url + "/guide/code-table3"
        # 직무/직업 코드용 url
        self.urls['job_code'] = self.base_url + "/guide/code-table4"

        self.rawHTMLs = {}
        self.requestRawHTML()
        self.code_table_created = False

    # 여기서부턴 soup 형식의 객체를 모두 raw_html(가공되지 않은 html)로 선언
    def requestRawHTML(self):
        keys = self.urls.keys()
        for key in tqdm(keys, total=len(keys)):
            raw_html = getResponsedHtml(self.urls[key], self.headers, self.num_of_tries, self.cache_folder, self.ignore_cache)
            self.rawHTMLs[key] = raw_html

    def _processTableFromRawHTML1(self, raw_html):
        table_dict = {}
        rawTables = raw_html.find_all('div', class_='tabpanel')

        for rawTable in rawTables:
            table_name = rawTable.find('h2').text
            table = rawTable.find('table')
            if table:
                rows = table.find_all('tr')
                columns = [col_name.text for col_name in rows[0].find_all('th')]
                data = [[cell.text for cell in row.find_all('td')] for row in rows[1:]]
                df = pd.DataFrame(data, columns=columns)
                table_dict[table_name] = df

        return table_dict
    
    def _processTableFromRawHTML2(self, raw_html):
        base_href = "/guide/code-table5?mcode="
        table_dict = {}
        mcodeClass = raw_html.find('ul', class_='wrap_tab type_row')
        
        table_name = '직무 테이블'
        columns = ['직무 상위 코드', '직무명']
        mcode_wrappers = mcodeClass.find_all('li')
        data = [[mcode_wrapper.a['href'].replace(base_href,""), mcode_wrapper.a.get_text(strip=True)] for mcode_wrapper in mcode_wrappers]

        m_df = pd.DataFrame(data, columns=columns)
        # print(m_df)
        table_dict[table_name] = m_df

        for row in m_df.iterrows():
            url = self.base_url + base_href + str(row[1]['직무 상위 코드'])
            # print(url)
            # print(urllib.parse.quote(url, safe=''))
            raw_html = getResponsedHtml(url, self.headers, self.num_of_tries, self.cache_folder, self.ignore_cache)

            _table_dict = self._processTableFromRawHTML1(raw_html)
            table_dict |= _table_dict

        return table_dict

    def processTableFromRawHTML(self):
        _a_code_table = {}
        keys = self.urls.keys()
        for key in tqdm(keys, total=len(keys)):
            if (key!='job_code'):
                _a_code_table |= self._processTableFromRawHTML1(self.rawHTMLs[key])
            else:
                _a_code_table |= self._processTableFromRawHTML2(self.rawHTMLs[key])

        # print(_a_code_table)
        jobCodeTable = JobCodeTable(
            _a_code_table['기획·전략 코드'],
            _a_code_table['마케팅·홍보·조사 코드'],
            _a_code_table['회계·세무·재무 코드'],
            _a_code_table['인사·노무·HRD 코드'],
            _a_code_table['총무·법무·사무 코드'],
            _a_code_table['IT개발·데이터 코드'],
            _a_code_table['디자인 코드'],
            _a_code_table['영업·판매·무역 코드'],
            _a_code_table['고객상담·TM 코드'],
            _a_code_table['구매·자재·물류 코드'],
            _a_code_table['상품기획·MD 코드'],
            _a_code_table['운전·운송·배송 코드'],
            _a_code_table['서비스 코드'],
            _a_code_table['생산 코드'],
            _a_code_table['건설·건축 코드'],
            _a_code_table['의료 코드'],
            _a_code_table['연구·R&D 코드'],
            _a_code_table['교육 코드'],
            _a_code_table['미디어·문화·스포츠 코드'],
            _a_code_table['금융·보험 코드'],
            _a_code_table['공공·복지 코드'],
        )

        self.code_table = CodeTable(
            _a_code_table['근무형태 코드'],
            _a_code_table['학력 코드'],
            _a_code_table['연봉 범위 코드'],
            _a_code_table['사람인 근무지/지역 코드'],
            _a_code_table['2차 근무지/지역 코드'],
            _a_code_table['1차 근무지/지역 코드'],
            _a_code_table['상위 산업/업종 코드'],
            _a_code_table['산업/업종 코드'],
            _a_code_table['업종 키워드 코드'],
            _a_code_table['직무 테이블'],
            jobCodeTable
        )

        self.code_table_created = True

    def getCodeTable(self):
        if self.code_table_created:
            return self.code_table
        else:
            return None


class WebScrapper(WebScarpperBase):
    def  __init__(self, code_table:CodeTable, base_url, headers, num_of_tries=5, cache_folder='./__htmlCache__'):
        '''
        code_table: CodeTable
        '''
        super().__init__(base_url, headers, num_of_tries, cache_folder)
        self.code_table = code_table
        self.urls['domestic_url'] = self.base_url + "/zf_user/jobs/list/domestic"
        self.urls['job_category_url'] = self.base_url + "/zf_user/jobs/list/job-category"
        self.rawHTMLs = {}
        self.job_data = {}

    def addParam2Url(self, url, param_dict):
        url += '?'
        for key in param_dict.keys():
            url += f'{key}={param_dict[key]}&'
        return url
    
    def getJobListHTMLFromHTML(self, raw_html):
        job_html_list_html = raw_html.find('div', class_='common_recruilt_list')
        if job_html_list_html is None:
            return None
        job_html_list_html = job_html_list_html.find('div', class_='list_body')
        return job_html_list_html.find_all('div', class_=lambda x: x and 'list_item' in x.split(), id=lambda y: y and y.startswith('rec-'))

    def _processItemData(self, item):
        return {
                "company_name": item.select_one(".col.company_nm .str_tit").get_text(strip=True) if item.select_one(".col.company_nm .str_tit") else None,
                "company_href": item.select_one(".col.company_nm .str_tit").get("href") if item.select_one(".col.company_nm .str_tit") else None,
                "main_corp": item.select_one(".col.company_nm .main_corp").get_text(strip=True) if item.select_one(".col.company_nm .main_corp") else None,
                "job_title": item.select_one(".col.notification_info .job_tit .str_tit").get_text(strip=True) if item.select_one(".col.notification_info .job_tit .str_tit") else None,
                "job_href": item.select_one(".col.notification_info .job_tit .str_tit").get("href") if item.select_one(".col.notification_info .job_tit .str_tit") else None,
                "job_sectors": [sector.get_text(strip=True) for sector in item.select(".job_meta .job_sector span")] if item.select(".job_meta .job_sector span") else None,
                "work_place": item.select_one(".col.recruit_info .work_place").get_text(strip=True) if item.select_one(".col.recruit_info .work_place") else None,
                "career": item.select_one(".col.recruit_info .career").get_text(strip=True) if item.select_one(".col.recruit_info .career") else None,
                "education": item.select_one(".col.recruit_info .education").get_text(strip=True) if item.select_one(".col.recruit_info .education") else None,
                "deadline": item.select_one(".col.support_info .support_detail .date").get_text(strip=True) if item.select_one(".col.support_info .support_detail .date") else None,
                "registered_days": item.select_one(".col.support_info .support_detail .deadlines").get_text(strip=True) if item.select_one(".col.support_info .support_detail .deadlines") else None,
                "loc_code": set(),
                "job_code": set(),
                "sal_code": int,
            }
    
    def processJobDataWithLocCode(self, job_html_list, loc_code, max_item_list):    
        if job_html_list is None:
            return False
        
        item_cnt = len(job_html_list)
        for item in tqdm(job_html_list, total=item_cnt):
            job_id = item.get("id")
            
            if job_id == None:
                continue
            
            if job_id not in self.job_data.keys():
                self.job_data[job_id] = self._processItemData(item)
            
            self.job_data[job_id]["loc_code"].add(loc_code)
        
        if item_cnt < max_item_list:
            return False
        return True

    def processJobDataWithJobCode(self, job_html_list, job_code, max_item_list):    
        if job_html_list is None:
            return False
            
        item_cnt = len(job_html_list)
        for item in tqdm(job_html_list, total=item_cnt):
            job_id = item.get("id")
            
            if job_id == None:
                continue
            
            if job_id not in self.job_data.keys():
                self.job_data[job_id] = self._processItemData(item)
            
            self.job_data[job_id]['job_code'].add(job_code)

        if item_cnt < max_item_list:
            return False
        return True

    def webScrapAllDomestic(self):
        print("시작")
        # 지역 별 순회
        loc_2_list = self.code_table.total_loc['2차 지역코드'].tolist()
        max_list_item = 1000
        
        for loc_2_code in tqdm(loc_2_list, total=len(loc_2_list)):
            param_dict = {}
            page_cnt = 1
            param_dict['page_count'] = max_list_item
            while(True):
                param_dict['page'] = page_cnt
                param_dict['loc_mcd'] = loc_2_code
                url = self.addParam2Url(self.urls['domestic_url'], param_dict)
                # print(url)
                raw_html = getResponsedHtml(url, self.headers, self.num_of_tries, self.cache_folder, self.ignore_cache)
                if not self.processJobDataWithLocCode(self.getJobListHTMLFromHTML(raw_html), loc_2_code, max_list_item):
                    break
                page_cnt += 1


    def webScrapAllJobCategory(self):
        print("시작")
        # 지역 별 순회
        job_code_list = self.code_table.jobCodeTable.get_total_dataframe()['직무 코드'].tolist()
        max_list_item = 1000
        
        for job_code in tqdm(job_code_list, total=len(job_code_list)):
            param_dict = {}
            page_cnt = 1
            param_dict['page_count'] = max_list_item
            while(True):
                param_dict['page'] = page_cnt
                param_dict['cat_kewd='] = job_code
                url = self.addParam2Url(self.urls['job_category_url'], param_dict)
                # print(url)
                raw_html = getResponsedHtml(url, self.headers, self.num_of_tries, self.cache_folder, self.ignore_cache)
                if not self.processJobDataWithJobCode(self.getJobListHTMLFromHTML(raw_html), job_code, max_list_item):
                    break
                page_cnt += 1


if __name__ == "__main__":
    code_url = "https://oapi.saramin.co.kr"
    base_url = "https://www.saramin.co.kr"
    
    # Robots.txt 방지용
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    wsct = WebScrapperCodeTable(code_url, headers)
    wsct.processTableFromRawHTML()
    
    code_table = wsct.getCodeTable()

    ws = WebScrapper(code_table, base_url, headers)
    ws.webScrapAllJobCategory()

    # table_dict = ws._processTableFromRawHTML(ws.rawHTMLs['job_code'])
    # print(len(table_dict))
    # for key in table_dict.keys():
    #     print(key)
    #     print(table_dict[key], end='\n\n')