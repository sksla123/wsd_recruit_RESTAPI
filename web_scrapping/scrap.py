from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Selenium 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 로드
url = "https://www.saramin.co.kr/zf_user/jobs/list/domestic"
driver.get(url)

# JavaScript 실행을 위한 대기 시간
time.sleep(5)

# 페이지 소스 가져오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

elements = soup.find_all(class_ = 'wrap_depth_category')
print(elements)

# # 여기에 원하는 데이터 추출 로직을 추가하세요
# # 예: 지역 카테고리 추출
# categories = soup.select('.wrap_depth_category .depth1_btn_wrapper')
# for category in categories:
#     print(category.text.strip())

# 브라우저 종료
driver.quit()