import platform
import os
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import aiofiles

host = 'https://qss-stock.devsecstudio.com/'
headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 71.0.3578.98 Safari / 537.36 OPR / 58.0.3135.132'
}
s = asyncio.BoundedSemaphore(10)


async def get_file(session, url):
    try:
        file_name = f'templates{os.path.sep}{url.split("/")[-1]}'
        if not os.path.exists('templates'):
            os.mkdir('templates')

        if os.path.exists(file_name):
            print(f'[2] {file_name} EXISTS')
            return

        async with s, session.get(url=url, headers=headers) as response:
            data = await response.read()

        async with aiofiles.open(file_name, 'wb') as file:
            await file.write(data)
            print(f'[0] {url} OK')
    except:
        print(f'[1] {url} FAILED')


async def collect_data(url):
    async with aiohttp.ClientSession() as session:
        r = await session.get(url=url, headers=headers)

        soup = BeautifulSoup(await r.text(), 'lxml')
        cards = soup.find_all('a', class_='btn btn-md btn-primary display-7')
        links = []
        for card in cards:
            links.append(f'{host}{card.get("href")}')

        tasks = []
        for link in links:
            task = asyncio.create_task(get_file(session, link))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(collect_data(f'{host}templates.php'))
