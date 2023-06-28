import requests
from bs4 import BeautifulSoup


headers = {
        "Host": "hh.ru",
        "User-Agent": "Safari",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
          }

URL = "https://hh.ru/search/vacancy?text={}&items_on_page=100"


def ExtractCntOfPages(vacancy):
    hh_request = requests.get(URL.format(vacancy), headers=headers)

    hh_soup = BeautifulSoup(hh_request.text, "html.parser")
    
    pages = []

    paginator = hh_soup.find_all("span", 
                            {"class": "pager-item-not-in-short-range",})
    for page in paginator:
        pages.append(int(page.find("a").text))
        
    return pages[-1]


def ExtractHHJobs(vacancy="python"):
    last_page = ExtractCntOfPages(vacancy)
    jobs = []
    for page in range(last_page):
        paginator = requests.get(f"{URL.format(vacancy)}&page={page}", 
                                 headers=headers)
        
        soup = BeautifulSoup(paginator.text, "html.parser")
        
        
        
        
