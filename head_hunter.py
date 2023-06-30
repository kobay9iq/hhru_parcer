import requests
from bs4 import BeautifulSoup
import html5lib

headers = {
    "Host": "hh.ru",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,\
        image/avif,image/webp,image/apng,*/*;\
        q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "navigate"
}

URL = "https://hh.ru/search/vacancy?text={}&items_on_page=20"


def ExtractCntOfPages(vacancy):
    hh_request = requests.get(URL.format(vacancy), headers=headers)

    hh_soup = BeautifulSoup(hh_request.text, "html5lib")

    pages = []

    paginator = hh_soup.find_all("span",
                                 {"class": "pager-item-not-in-short-range", })
    for page in paginator:
        pages.append(int(page.find("a").text))

    return pages[-1]


def ExtractAllVacancies(vacancy="python"):
    last_page = ExtractCntOfPages(vacancy)
    jobs = []

    for page in range(last_page):
        print(f"Парсинг страницы {page}")
        try:
            paginator = requests.get(f"{URL.format(vacancy)}&page={page}",
                                     headers=headers)
            print(paginator.status_code)
        except:
            print(
                f"Не удалось загрузить страницу под номером {page}")
            continue

        soup = BeautifulSoup(paginator.text, "html5lib")
        raw_vacancies = soup.find_all("div", {
            "class": "vacancy-serp-item__layout"
        })

        for result in raw_vacancies:
            jobs.append(ExtractVacancyInfo(result))

    return jobs


def ExtractVacancyInfo(html):
    tittle = html.find("a")
    tittle = NoneChecker(tittle)

    company = html.find("div", {"class":
                                "vacancy-serp-item__meta-info-company"})
    company = NoneChecker(company)

    city = html.find("div", {"data-qa":
                             "vacancy-serp__vacancy-address"})
    city = NoneChecker(city)
    if "," in city:
        city = city.split(",")[0]

    experience = html.find("div", {"data-qa":
                                   "vacancy-serp__vacancy-work-experience"})
    experience = NoneChecker(experience)

    salary = html.find("span", {"data-qa":
                               "vacancy-serp__vacancy-compensation"})
    salary = NoneChecker(salary)

    link = html.find("a")["href"]

    return {
        "tittle": tittle,
        "company": company,
        "city": city,
        "experience": experience,
        "salary": salary,
        "link": link,
    }


def NoneChecker(html):
    if html is not None:
        html = html.text.replace("\\xa0", " ").strip()
    else:
        html = "Нет данных"
    return html
