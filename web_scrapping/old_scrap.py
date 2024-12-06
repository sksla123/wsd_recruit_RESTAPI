import requests
from bs4 import BeautifulSoup

class WebScrapper:
    def  __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.setLocationUrl()

    def setLocationUrl(self):
        location_route = "/zf_user/jobs/list/domestic"
        self.locationUrl = self.base_url + location_route

    def getLocationID(self):
        response = requests.get(self.locationUrl + "?page=1&loc_mcd=101000&cat_cd=&search_optional_item=n&search_done=y&panel_type=&search_type=search&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1&tab_type=search&cat_mcls=2&type=job-category&is_sp_recruit=0", headers=self.headers)
        # data = response.json()

        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(class_ = 'wrap_depth_category')

        print(elements)
        # print(data)
        

if __name__ == "__main__":
    base_url = "https://www.saramin.co.kr"
    # robot.txt 회피용
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    ws = WebScrapper(base_url=base_url, headers=headers)

    ws.getLocationID()