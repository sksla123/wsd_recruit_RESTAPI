import os
import time
import urllib.parse
import pandas as pd

from tqdm.auto import tqdm

import requests
from bs4 import BeautifulSoup

from dataclasses import dataclass

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
        print('cache에서 불러옴')
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
                print('cache 저장됨')
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
        self.ignore_cache = False

        self.urls = {}
        
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
        self.code_table = {}

    def setIgnoreCache(self, flag=False):
        self.ignore_cache = flag

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

        print(_a_code_table)


    '''
    사람인 파라미터 분석

    경력:
        무관 (exp_none=y&)
        신입 (exp_cd=1&)
        경력 (exp_cd=2&)
        // 기간 (0~20)
        1년 이하 (exp_cd=2&exp_max=1&)
        a년 이상 b년 이하 (exp_cd=2&exp_min=a&exp_max=b&), (a, b = 1~20)
        20년 이상 (exp_cd=2&exp_min=20)


    학력:
        무관 (edu_none=y&)
        고교 졸업 이하 (edu_max=9&)
        박사 졸업 이상 (edu_min=5&)

        고등학교 졸업 이상 (edu_min=6)
        (edu_min=6&edu_max=13&)
        대학원 박사 졸업 이하 (edu_max=13&)

    연봉1:
        회사내규에 따름 (sal_cd=0&)
        면접 후 결정 (sal_cd=99&)

    연봉2:
        2400만원 이상 (sal_min=8&)
        2600만원 이상 (sal_min=9&)
        2800만원 이상 (sal_min=10&)
        3000만원 이상 (sal_min=11&)
        3200만원 이상 (sal_min=12&)
        3400만원 이상 (sal_min=13&)
        3600만원 이상 (sal_min=14&)
        3800만원 이상 (sal_min=15&)
        4000만원 이상 (sal_min=16&)
        5000만원 이상 (sal_min=17&)
        6000만원 이상 (sal_min=18&)
        7000만원 이상 (sal_min=19&)
        8000만원 이상 (sal_min=20&)
        9000만원 이상 (sal_min=11&)
        1억원 이상 (sal_min=22&)
        
    재택근무 가능:
        재택근무 불가 (work_type=0&)
        재택근무 가능 (work_type=1&)

    기업 형태:
        기업 크기:
            대기업 (company_type=scale001&)
            매출1000대기업 (company_type=scale002&)
            중견기업 (company_type=scale003&)
            중소기업 (company_type=scale004&)
            스타트업 (company_type=scale005&)
            개인사업자 (company_type=scale006&)
        기업 분류:
            외국계(법인/투자) (company_type=foreign)
            공사·공기업 (company_type=public)
            연구소 (company_type=laboratory)
            학교·교육기관 (company_type=school)
            사회복지기관 (company_type=social-welfare)
            금융기관 (company_type=banking-organ)
            비영리단체,협회 (company_type=nonprofit)
            병원,의료기관 (company_type=medical-institution)
        기업 상장 위치:
            코스닥 (company_type=kosdaq)
            코스피 (company_type=kospi)
            코넥스 (company_type=konex)
        기업 법인 형태:
            주식회사 (company_type=stock)
            유한회사 (company_type=incorporated)
            협동조합 (company_type=cooperative)
            사단법인 (company_type=corporate-juridical-person)
            재단법인 (company_type=foundation)
            외부감사법인 (company_type=Cex_audit)
        기업 기타:
           병역특례 인증업체 (company_type=military)
           수출업기업 (company_type=ex_import)

    근무 형태:
        (job_type=a&) (a 8~22)

    근무 시간대:
        주 5일(월~금) (workday=wsh010)
        주 6일(월~토) (workday=wsh030)
        주 3일(격일제) (workday=wsh040)
        유연근무제 (workday=wsh50)
        면접 후 결정 (workday=wsh090)

    복리 후생:
        건강검진 (welfare_cd=corp407)
        의료비지원(본인) (welfare_cd=corp408)
        금연수당 (welfare_cd=corp409)
        직원대출제도 (welfare_cd=corp411)
        각종 경조사 지원 (welfare_cd=corp417)
        단체 상해보험 (welfare_cd=corp419)
        의료비지원(가족) (welfare_cd=corp439)
        체력단련실운영 (welfare_cd=corp440)
        헬스비 지급 (welfare_cd=corp441)
        무료진료지정병원 (welfare_cd=corp442)
        본인학자금 (welfare_cd=corp486)
        업무활동비 지급 (welfare_cd=corp487)
        문화생활비 (welfare_cd=corp488)
        통신비 지원 (welfare_cd=corp489)
        결혼준비 지원 (welfare_cd=corp490)
        해외여행 지원 (welfare_cd=corp491)
        선택적복리후생 (welfare_cd=corp492)
        복지카드/포인트 (welfare_cd=corp495)
        난임 치료 지원 (welfare_cd=corp496)
        주요 제품 직원 할인 (welfare_cd=corp497)
        자녀학자금 (welfare_cd=corp498)
        사내 결혼식장 제공 (welfare_cd=corp534)
        내일채움공제 (welfare_cd=corp537)
        퇴직연금 (welfare_cd=corp400)
        인센티브제 (welfare_cd=corp401)
        상여금 (welfare_cd=corp402)
        장기근속자 포상 (welfare_cd=corp403)
        우수사원포상 (welfare_cd=corp404)
        스톡옵션 (welfare_cd=corp405)
        퇴직금 (welfare_cd=corp406)
        성과급 (welfare_cd=corp420)
        야근수당 (welfare_cd=corp421)
        휴일(특근)수당 (welfare_cd=corp422)
        연차수당 (welfare_cd=corp423)
        직책수당 (welfare_cd=corp424)
        자격증수당 (welfare_cd=corp425)
        장기근속수당 (welfare_cd=corp426)
        위험수당 (welfare_cd=corp427)
        가족수당 (welfare_cd=corp428)
        4대 보험 (welfare_cd=corp499)
        명절선물/귀향비 (welfare_cd=corp434)
        창립일선물지급 (welfare_cd=corp435)
        생일선물/파티 (welfare_cd=corp436)
        크리스마스 선물 (welfare_cd=corp437)
        결혼기념일선물 (welfare_cd=corp438)
        도서 무제한 제공 (welfare_cd=corp500)
        임신/출산 선물 (welfare_cd=corp501)
        웰컴키트 지급 (welfare_cd=corp502)
        생일자 조기퇴근 (welfare_cd=corp503)
        장기근속 선물 (welfare_cd=corp532)
        창립일행사 (welfare_cd=corp100)
        우수사원시상식 (welfare_cd=corp101)
        워크샵 (welfare_cd=corp102)
        플레이샵 (welfare_cd=corp103)
        신규 입사자 교육(OJT) (welfare_cd=corp200)
        직무능력향상교육 (welfare_cd=corp201)
        리더십 강화교육 (welfare_cd=corp202)
        해외연수지원 (welfare_cd=corp203)
        도서구입비지원 (welfare_cd=corp204)
        MBA과정지원 (welfare_cd=corp205)
        멘토링제도 (welfare_cd=corp206)
        외국어 교육 지원 (welfare_cd=corp207)
        사이버연수원운영 (welfare_cd=corp208)
        자격증취득지원 (welfare_cd=corp209)
        교육비 지원 (welfare_cd=corp210)
        자기계발비 지원 (welfare_cd=corp211)
        구내식당(사원식당) (welfare_cd=corp413)
        점심식사 제공 (welfare_cd=corp415)
        저녁식사 제공 (welfare_cd=corp416)
        사내동호회 운영 (welfare_cd=corp418)
        사우회(경조사회) (welfare_cd=corp429)
        아침식사 제공 (welfare_cd=corp469)
        간식 제공 (welfare_cd=corp470)
        식비 지원 (welfare_cd=corp471)
        음료제공(차, 커피) (welfare_cd=corp472)
        해외주재원 제도 (welfare_cd=corp493)
        우리사주제도 (welfare_cd=corp494)
        해외 워크샵 (welfare_cd=corp504)
        점심시간 연장제도 (welfare_cd=corp505)
        취미 프로그램 운영 (welfare_cd=corp506)
        가족 초청 행사 (welfare_cd=corp507)
        신규입사자 멘토 제도 (welfare_cd=corp531)
        컨퍼런스 개최 (welfare_cd=corp536)
        수유실 (welfare_cd=corp443)
        사내 어린이집 운영 (welfare_cd=corp444)
        휴게실 (welfare_cd=corp449)
        수면실 (welfare_cd=corp450)
        회의실 (welfare_cd=corp451)
        공기청정기 (welfare_cd=corp452)
        카페테리아 (welfare_cd=corp453)
        게임기 (welfare_cd=corp454)
        전용 사옥 (welfare_cd=corp455)
        사내 정원 (welfare_cd=corp457)
        건물 내 경사로 (welfare_cd=corp458)
        휠체어용 난간 (welfare_cd=corp459)
        유도점자블록 (welfare_cd=corp460)
        장애인 화장실 (welfare_cd=corp461)
        장애인 전용주차장 (welfare_cd=corp462)
        장애인 엘리베이터 (welfare_cd=corp463)
        비상경보장치 (welfare_cd=corp464)
        문턱 없음 (welfare_cd=corp465)
        유니폼지급 (welfare_cd=corp468)
        스마트기기 (welfare_cd=corp481)
        노트북 (welfare_cd=corp482)
        사원증 (welfare_cd=corp483)
        자회사 제품할인 (welfare_cd=corp484)
        콘도/리조트 이용권 (welfare_cd=corp485)
        사내도서관 (welfare_cd=corp508)
        사무용품 지급 (welfare_cd=corp509)
        최고 성능 컴퓨터 (welfare_cd=corp510)
        안마실/안마의자 (welfare_cd=corp511)
        사내 의원/약국 (welfare_cd=corp512)
        스탠딩 책상 (welfare_cd=corp513)
        비자 발급 지원 (welfare_cd=corp538)
        무제한 연차 (welfare_cd=corp309)
        노조/노사협의회 (welfare_cd=corp430)
        수평적 조직문화 (welfare_cd=corp431)
        회식강요 안함 (welfare_cd=corp432)
        야근강요 안함 (welfare_cd=corp433)
        자유복장 (welfare_cd=corp466)
        캐주얼데이 (welfare_cd=corp467)
        자유로운 연차사용 (welfare_cd=corp514)
        님/닉네임 문화 (welfare_cd=corp515)
        출산 장려 (welfare_cd=corp516)
        칼퇴근 보장 (welfare_cd=corp518)
        반려동물 동반출근 (welfare_cd=corp519)
        문화 회식 (welfare_cd=corp520)
        사내연애 장려 (welfare_cd=corp533)
        기숙사 운영 (welfare_cd=corp410)
        차량유류비지급 (welfare_cd=corp412)
        통근버스 운행 (welfare_cd=corp414)
        사택제공 (welfare_cd=corp473)
        사원아파트 임대 (welfare_cd=corp474)
        주택자금 융자 (welfare_cd=corp475)
        야간교통비지급 (welfare_cd=corp476)
        주차장제공 (welfare_cd=corp477)
        주차비지원 (welfare_cd=corp478)
        회사차량 있음 (welfare_cd=corp479)
        탄력근무제 (welfare_cd=corp480)
        주거비 지원 (welfare_cd=corp521)
        전세자금 대출 (welfare_cd=corp522)
        출퇴근 교통비 지원 (welfare_cd=corp523)
        재택근무 (welfare_cd=corp524)
        주 52시간제 준수 (welfare_cd=corp525)
        주 40시간제 시행 (welfare_cd=corp526)
        주4.5일 (welfare_cd=corp527)
        주4일 (welfare_cd=corp528)
        자율 근무제 (welfare_cd=corp535)
        연차 (welfare_cd=corp300)
        여름휴가 (welfare_cd=corp301)
        경조휴가제 (welfare_cd=corp302)
        반차 (welfare_cd=corp303)
        Refresh휴가 (welfare_cd=corp304)
        창립일휴무 (welfare_cd=corp305)
        근로자의 날 휴무 (welfare_cd=corp306)
        휴가비지원 (welfare_cd=corp307)
        포상휴가 (welfare_cd=corp308)
        산전 후 휴가 (welfare_cd=corp445)
        육아휴직 (welfare_cd=corp446)
        남성출산휴가 (welfare_cd=corp447)
        보건휴가 (welfare_cd=corp448)
        휴양시설 제공 (welfare_cd=corp456)
        패밀리데이 (welfare_cd=corp529)
        시간제 연차 (welfare_cd=corp530)
        공휴일 휴무 (welfare_cd=corp310)

    '''

    

if __name__ == "__main__":
    code_url = "https://oapi.saramin.co.kr"
    
    ws = WebScrapperCode(base_url=code_url)

    ws.processTableFromRawHTML()

    # table_dict = ws._processTableFromRawHTML(ws.rawHTMLs['job_code'])
    # print(len(table_dict))
    # for key in table_dict.keys():
    #     print(key)
    #     print(table_dict[key], end='\n\n')