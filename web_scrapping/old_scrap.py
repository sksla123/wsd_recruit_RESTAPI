import os
import requests
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import time

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
    cache_file_path = os.path.join(cache_folder, f'{safe_file_name}.txt')

    os.makedirs(cache_folder, exist_ok=True)

    if (not ignore_cache and os.path.exists(cache_file_path)):
        with open(cache_file_path, 'r') as f:
            html = BeautifulSoup(f.read(), 'html.parser')
        return html
    else:
        while(num_of_tries != 0):
            response = requests.get(url, headers=headers)
            if(response.status_code != 200):
                num_of_tries -= 1
                time.sleep(1) # 임시 차단되었을 가능성이 있으므로 1초 쉬고 재시도
                continue
            html = BeautifulSoup(response.text, 'html.parser')
            with open(cache_file_path, 'w') as f:
                print(html, file=f)
            return html
    
    return None

class WebScrapper:
    def  __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.setLocationUrl()

    def setLocationUrl(self):
        location_route = "/guide/code-table1"
        self.locationUrl = self.base_url + location_route

    def getLocationID(self):
        response = requests.get(self.locationUrl, headers=self.headers)
        # data = response.json()

        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        # elements = soup.find_all(class_ = 'wrap_depth_category')

        # print(elements)
        # print(data)
        

class WebScrapperCode():
    def  __init__(self, base_url, headers, num_of_tries=5, cache_folder='./__htmlCache__'):
        self.base_url = base_url
        self.headers = headers
        self.num_of_tries = num_of_tries
        self.cache_folder = cache_folder

        self.urls = {}
        
        # 근무형태/학력/연봉 코드용 url
        self.urls['extra_code'] = self.base_url + "/guide/code-table1"
        # 근무지/지역 코드용 url
        self.urls['loc_code'] = self.base_url + "/guide/code-table2"
        # 산업/업종 코드용 url
        self.urls['industry_code'] = self.base_url + "/guide/code-table3"
        # 직무/직업 코드용 url
        self.urls['job_code'] = self.base_url + "/guide/code-table4"

        self.rawHTML = {}
        self.code_tables = {}
        self.requestRawHTML()

    # 여기서부턴 soup 형식의 객체를 모두 raw_html(가공되지 않은 html)로 선언
    def requestRawHTML(self, ignore_cache=False):
        keys = self.urls.keys()
        for key in tqdm(keys, total=len(keys)):
            raw_html = getResponsedHtml(self.urls[key], self.headers, self.num_of_tries, self.cache_folder, ignore_cache)
            self.rawHTML[key] = raw_html

    def _processTableFromRawHTML(self, raw_html):
        table_dict = {}
        rawTables = raw_html.find_all('div', class_='tabpanel')

        for rawTable in rawTables:
            table_name = rawTable.find('h2').text
            table = rawTable.find('table')
            if table:
                rows = table.find_all('tr')
                headers = [header.text for header in rows[0].find_all('th')]
                data = [[cell.text for cell in row.find_all('td')] for row in rows[1:]]
                df = pd.DataFrame(data, columns=headers)
                table_dict[table_name] = df

        return table_dict

    

if __name__ == "__main__":
    code_url = "https://oapi.saramin.co.kr"
    
    # robot.txt 회피용
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    ws = WebScrapperCode(base_url=code_url, headers=headers)

    raw_html = ws.rawHTML['industry_code']
    table_dict = ws._processTableFromRawHTML(raw_html)
    print(len(table_dict))
    for key in table_dict.keys():
        print(key)
        print(table_dict[key], end='\n\n')