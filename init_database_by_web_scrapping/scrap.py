import re
import os
import time
import urllib.parse
import pandas as pd

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from tqdm.auto import tqdm

import requests
from bs4 import BeautifulSoup

import gzip

from .util import JobDictToExcel, save_to_pickle, now_korea
from .job_dataclasses import JobCodeTable, CodeTable

import argparse

def getResponsedHtml(url, 
                     headers = {
                            # Robots.txt 방지용
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                         }, 
                     num_of_tries=5, 
                     cache_folder='./__htmlCache__',
                     ignore_cache=False,
                     stop_caching=False,
                     ):
    '''
    반복된 요청으로 차단되지 않도록, cache 폴더에 html을 백업해두고 필요시 url로 요청하지 않고 폴더에서 꺼내옴
    만약 오래된 cache 파일을 무시하게 하고 싶으면, ignore_cache 플래그를 True로 설정
    cache 저장을 하고 싶지 않다면, stop_caching을 True로 설정
    '''
    
    safe_file_name = urllib.parse.quote(url, safe='')
    cache_file_path = os.path.join(cache_folder, f'{safe_file_name}.txt.gz')

    os.makedirs(cache_folder, exist_ok=True)
    # print("캐쉬 파일 경로:", cache_file_path)
    # print("ignore_cache:", ignore_caching)
    # print("stop_caching:", ignore_caching)

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
            if not stop_caching:
                with gzip.open(cache_file_path, 'wt', encoding='utf-8') as f:
                    f.write(str(html))
                    # print('cache 저장됨')
            return html
    
    return None



class WebScarpperBase():
    def  __init__(self, base_url, headers, num_of_tries=5, cache_folder='./__htmlCache__'):
        self.base_url = base_url
        self.headers = headers
        self.num_of_tries = num_of_tries
        self.cache_folder = cache_folder
        self.ignore_cache = False
        self.stop_caching = True
        self.isTest = False
        
        self.urls={}

    def setIgnoreCache(self, flag=False):
        self.ignore_cache = flag

    def setStopCaching(self, flag=True):
        self.stop_caching = flag

    def set_test_mode(self, flag=False):
        self.isTest = flag
        
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
        self.urls['job_code'] = self.base_url + "/guide/code-table5"

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

    def __getNowKoreaTime(self):
        korea_time = datetime.now(ZoneInfo("Asia/Seoul"))
        return korea_time
        
    def __getDefaultTime(self):
        unix_epoch = datetime(1970, 1, 1, tzinfo=ZoneInfo("UTC"))
        korea_time = unix_epoch.astimezone(ZoneInfo("Asia/Seoul"))
        
        return korea_time.strftime("%Y-%m-%d")

    def _preprocessDeadline(self, date_str):
        if None:
            return self.__getDefaultTime()

        cur_korea_time = self.__getNowKoreaTime()

        if re.match(r'\(\d+\)시 마감', date_str):
            return cur_korea_time.strftime("%Y-%m-%d")

        # 2. D-(숫자)
        d_match = re.match(r'D-(-?\d+)', date_str)
        if d_match:
            days_offset = int(d_match.group(1))  # 추출된 숫자
            deadline_date = cur_korea_time + timedelta(days=days_offset)
            return deadline_date.strftime("%Y-%m-%d")
    
        # 3. 오늘마감
        if date_str == "오늘마감":
            return cur_korea_time.strftime("%Y-%m-%d")
    
        # 4. 내일마감
        if date_str == "내일마감":
            deadline_date = cur_korea_time + timedelta(days=1)
            return deadline_date.strftime("%Y-%m-%d")

        mm_dd_match = re.match(r'~(\d{2})\.(\d{2})\(\w\)', date_str)

        current_year = cur_korea_time.year
        if mm_dd_match:
            month = int(mm_dd_match.group(1))
            day = int(mm_dd_match.group(2))
            deadline_date = datetime(current_year, month, day, tzinfo=ZoneInfo("Asia/Seoul"))
            
            # 현재 날짜보다 과거라면 내년으로 설정
            if deadline_date < cur_korea_time:
                deadline_date = datetime(current_year + 1, month, day, tzinfo=ZoneInfo("Asia/Seoul"))
            
            return deadline_date.strftime("%Y-%m-%d")

    def _preprocessUpdateDate(self, date_str):
        if not date_str:
            return self.__getDefaultTime()

        cur_korea_time = self.__getNowKoreaTime()
        
        match1 = re.search(r'(\d+)일 전 등록', date_str)
        match2 = re.search(r'(\d+)일 전 수정', date_str)

        if match1:
            days_ago = int(match1.group(1))
        elif match2:
            days_ago = int(match2.group(1))
        else:
            return cur_korea_time.strftime("%Y-%m-%d")
        
        c_date = cur_korea_time - timedelta(days=days_ago)
        
        return c_date.strftime("%Y-%m-%d")
        
    def __removeUpperArrow(self, input_string):
        if '↑' in input_string:
            input_string = input_string.replace('↑', '')
            return 1, input_string
        return 0, input_string

    def _preprocessEdu(self, input_string):
        # 입력 예시: ['고졸', '대학(2,3년)', '대학교(4년)', '석사', '박사', '학력무관']
        flag, input_string = self.__removeUpperArrow(input_string)
        
        if '고졸' in input_string:
            edu_code = 1  # 고졸
        elif '대학(2,3년)' in input_string:
            edu_code = 2  # 대학(2,3년)
        elif '대학교(4년)' in input_string:
            edu_code = 3  # 대학교(4년)
        elif '석사' in input_string:
            edu_code = 4  # 석사
        elif '박사' in input_string:
            edu_code = 5  # 박사
        else:
            edu_code = 0  # 기본값은 학력무관
            
        return flag, edu_code
        
    def _processItemData(self, item):
        data = {
                "company_name": item.select_one(".col.company_nm .str_tit").get_text(strip=True) if item.select_one(".col.company_nm .str_tit") else None,
                "company_href": item.select_one(".col.company_nm .str_tit").get("href") if item.select_one(".col.company_nm .str_tit") else None,
                "main_corp": item.select_one(".col.company_nm .main_corp").get_text(strip=True) if item.select_one(".col.company_nm .main_corp") else None,
                "job_title": item.select_one(".col.notification_info .job_tit .str_tit").get_text(strip=True) if item.select_one(".col.notification_info .job_tit .str_tit") else None,
                "job_href": item.select_one(".col.notification_info .job_tit .str_tit").get("href") if item.select_one(".col.notification_info .job_tit .str_tit") else None,
                "job_sectors": [sector.get_text(strip=True) for sector in item.select(".job_meta .job_sector span")] if item.select(".job_meta .job_sector span") else None,
                "work_place": item.select_one(".col.recruit_info .work_place").get_text(strip=True) if item.select_one(".col.recruit_info .work_place") else None,
                "career": item.select_one(".col.recruit_info .career").get_text(strip=True) if item.select_one(".col.recruit_info .career") else None,
                "education": item.select_one(".col.recruit_info .education").get_text(strip=True) if item.select_one(".col.recruit_info .education") else None,
                "edu_code": 0,
                "edu_upper": 0,
                "deadline": self._preprocessDeadline(item.select_one(".col.support_info .support_detail .date").get_text(strip=True) if item.select_one(".col.support_info .support_detail .date") else None),
                "registered_days": self._preprocessUpdateDate(item.select_one(".col.support_info .support_detail .deadlines").get_text(strip=True) if item.select_one(".col.support_info .support_detail .deadlines") else None),
                "loc_code": set(),
                "job_code": set(),
                "sal_code": 100,
            }

        flag, edu_code = self._preprocessEdu(data['education'])
        data['edu_code'] = edu_code
        data['edu_upper'] = flag
        
        return data
    
    def processJobDataWithLocCode(self, job_html_list, loc_code, max_item_list, sal_code=None):    
        if job_html_list is None:
            return False
        
        item_cnt = len(job_html_list)
        for item in job_html_list:
            job_id = item.get("id")
            
            if job_id == None:
                continue
            
            if job_id not in self.job_data.keys():
                self.job_data[job_id] = self._processItemData(item)
            
            self.job_data[job_id]["loc_code"].add(loc_code)

            if sal_code is not None:
                self.job_data[job_id]["sal_code"] = sal_code
        
        if item_cnt < max_item_list:
            return False
        return True

    def processJobDataWithJobCode(self, job_html_list, job_code, max_item_list, sal_code=None):    
        if job_html_list is None:
            return False
            
        item_cnt = len(job_html_list)
        for item in job_html_list:
            job_id = item.get("id")
            
            if job_id == None:
                continue
            
            if job_id not in self.job_data.keys():
                self.job_data[job_id] = self._processItemData(item)
            
            self.job_data[job_id]['job_code'].add(job_code)

            if sal_code is not None:
                self.job_data[job_id]["sal_code"] = sal_code

        if item_cnt < max_item_list:
            return False
        return True

    def webScrapAllDomestic(self):
        print("시작")
        # 지역 별 순회
        loc_2_list = self.code_table.total_loc['2차 지역코드'].tolist()
        max_list_item = 1000

        cnt_for_test = 0
        for loc_2_code in tqdm(loc_2_list, total=len(loc_2_list)):
            if self.isTest and cnt_for_test >= 2:
                break
                
            param_dict = {}
            page_cnt = 1
            param_dict['page_count'] = max_list_item
            while(True):
                param_dict['page'] = page_cnt
                param_dict['loc_cd'] = loc_2_code
                url = self.addParam2Url(self.urls['domestic_url'], param_dict)
                # print(url)
                raw_html = getResponsedHtml(url, self.headers, self.num_of_tries, self.cache_folder, self.ignore_cache, self.stop_caching)
                if not self.processJobDataWithLocCode(self.getJobListHTMLFromHTML(raw_html), loc_2_code, max_list_item):
                    break
                page_cnt += 1
            cnt_for_test += 1

    def webScrapAllJobCategory(self):
        print("시작")
        # 지역 별 순회
        job_code_list = self.code_table.jobCodeTable.get_total_dataframe()['직무 코드'].tolist()
        max_list_item = 1000
        
        cnt_for_test = 0
        for job_code in tqdm(job_code_list, total=len(job_code_list)):
            if self.isTest and cnt_for_test >= 2:
                break
            param_dict = {}
            page_cnt = 1
            param_dict['page_count'] = max_list_item
            while(True):
                param_dict['page'] = page_cnt
                param_dict['cat_kewd'] = job_code
                url = self.addParam2Url(self.urls['job_category_url'], param_dict)
                # print(url)
                raw_html = getResponsedHtml(url, self.headers, self.num_of_tries, self.cache_folder, self.ignore_cache, self.stop_caching)
                if not self.processJobDataWithJobCode(self.getJobListHTMLFromHTML(raw_html), job_code, max_list_item):
                    break
                page_cnt += 1
            cnt_for_test += 1

    def webScrapAllJobCategoryWithSalData(self):
        print("시작")
        # 지역 별 순회
        job_code_list = self.code_table.jobCodeTable.get_total_dataframe()['직무 코드'].tolist()
        max_list_item = 1000

        cnt_for_test = 0
        for job_code in tqdm(job_code_list, total=len(job_code_list)):
            if self.isTest and cnt_for_test >= 2:
                break
            for sal_code in range(17):
                param_dict = {}
                if sal_code == 0:
                    param_dict['sal_cd'] = 0
                elif sal_code == 1:
                    param_dict['sal_cd'] = 99
                else:
                    param_dict['sal_min'] = sal_code + 6
                page_cnt = 1
                param_dict['page_count'] = max_list_item
                while(True):
                    param_dict['page'] = page_cnt
                    param_dict['cat_kewd'] = job_code
                    url = self.addParam2Url(self.urls['job_category_url'], param_dict)
                    # print(url)
                    raw_html = getResponsedHtml(url, self.headers, self.num_of_tries, self.cache_folder, self.ignore_cache, self.stop_caching)
                    if not self.processJobDataWithJobCode(self.getJobListHTMLFromHTML(raw_html), job_code, max_list_item, sal_code):
                        break
                    page_cnt += 1
            cnt_for_test += 1

def startWebScrapping(save_folder="./data", file_name = "data", ignore_cache=False, stop_caching=True, isTest=False):
    code_url = "https://oapi.saramin.co.kr" # CodeTable 관련 값을 받을 수 있는 url
    base_url = "https://www.saramin.co.kr" # 실제 사람인 베이스 주소

    # Robots.txt 방지용
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    wsct = WebScrapperCodeTable(code_url, headers)
    wsct.processTableFromRawHTML()
    wsct.setIgnoreCache(ignore_cache)
    wsct.setStopCaching(stop_caching)
    code_table = wsct.getCodeTable()
    
    ws = WebScrapper(code_table, base_url, headers)
    ws.setIgnoreCache(ignore_cache)
    ws.setStopCaching(stop_caching)
    ws.set_test_mode(isTest)
    ws.webScrapAllJobCategoryWithSalData()
    ws.webScrapAllDomestic()
    
    korea_time = datetime.now(ZoneInfo("Asia/Seoul"))
    timestamp = korea_time.strftime("%Y%m%d%H%M%S")
    backup_file_path = os.path.join(save_folder, f"{timestamp}_{file_name}_backup.pkl")
    backup_code_table_file_path = os.path.join(save_folder, f"{timestamp}_codetable_{file_name}_backup.pkl")
    
    save_to_pickle(ws.job_data, backup_file_path)
    save_to_pickle(wsct.code_table, backup_code_table_file_path)

    excel_file_path = os.path.join(save_folder, f"{timestamp}_{file_name}.xlsx")
    converter = JobDictToExcel(ws.job_data)

    converter.convert_to_excel(excel_file_path)
    
    wsct.setIgnoreCache()
    wsct.setStopCaching()
    ws.setIgnoreCache()
    ws.setStopCaching()
    ws.set_test_mode()
    
    return wsct, ws


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test script with isTest argument.")
    parser.add_argument('--isTest', action='store_true', help='Enable test mode.')
    
    args = parser.parse_args()

    if args.isTest:
        print("테스트 모드로 동작합니다.")
    
    # Jupyter Notebook 환경인지 확인
    if '__file__' in globals():
        # 일반 Python 스크립트에서는 __file__ 사용
        current_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        # Jupyter Notebook 환경에서는 os.getcwd() 사용
        current_dir = os.getcwd()
    
    # data 디렉토리 경로 결합
    dir_path = os.path.join(current_dir, "data")
    
    # 디렉토리 생성 (이미 존재하면 무시)
    os.makedirs(dir_path, exist_ok=True)

    wsct, ws = startWebScrapping(save_folder=dir_path, file_name="data", ignore_cache=False, stop_caching=False, isTest=args.isTest)

    