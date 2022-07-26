import requests
import os
from bs4 import BeautifulSoup

host = 'https://qss-stock.devsecstudio.com/'
headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 71.0.3578.98 Safari / 537.36 OPR / 58.0.3135.132'
}


def get_file(url):
    try:
        file_name = f'templates{os.path.sep}{url.split("/")[-1]}'
        if not os.path.exists('templates'):
            os.mkdir('templates')
        if os.path.exists(file_name):
            return 'EXISTS'
        response = requests.get(url=url, headers=headers)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return 'OK'
    except Exception as _ex:
        return 'FAILED'


def collect_data(url):
    if not os.path.exists('index.htm'):
        r = requests.get(url=url, headers=headers)
        src = r.text
        with open('index.htm', 'w', encoding="utf-8") as file:
            file.write(src)
    else:
        with open('index.htm', 'r', encoding="utf-8") as file:
            src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('a', class_='btn btn-md btn-primary display-7')
    links = []
    for card in cards:
        links.append(f'{host}{card.get("href")}')

    for cnt, link in enumerate(links):
        print(f'Downloading {cnt+1} of {len(links)} ... {get_file(link)}')


if __name__ == "__main__":
    collect_data(f'{host}templates.php')
