from back.session import read_session, get_cookie
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import sys

def cookie_expired():
    url = "https://sonaveeb.ee/worddetails/unif/244181"

    payload = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:107.0) Gecko/20100101 Firefox/107.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://sonaveeb.ee/search/unif/dlall/dsall/tere/1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Cookie": f"JSESSIONID={read_session()}"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    check = soup.find(class_='home-page-content')
    if check == None: #correct page found, cookie is ok
        return False
    else: #autoreturn to main page, cookie expired
        return True
