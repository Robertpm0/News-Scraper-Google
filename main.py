from wsgiref import headers
import numpy as np
import requests, urllib.parse, lxml
from bs4 import BeautifulSoup
import pandas as pd


searchThis = "SOL" # enter topic you would like scrape via Google.

def paginate(url, previous_url=None):
    if url == previous_url: return
    headers = {
        "User-Agent": "" # INSERT YOUR USER AGENT HERE
    }
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    yield soup

    next_page_node = soup.select_one('a#pnnext')

    if next_page_node is None: return

    next_page_url = urllib.parse.urljoin('https://www.google.com/', next_page_node['href'])
    yield from paginate(next_page_url)
data = []
def scrape():
    pages = paginate(f"https://www.google.com/search?hl=en-US&q={searchThis}&tbm=nws")
    for soup in pages:
        print(f'Current page: {int(soup.select_one(".YyVfkd").text)}\n')

        for result in soup.select('.WlydOe'):
            title = result.select_one('.nDgy9d').text
            link = result['href']
            source = result.select_one('.NUnG9d span').text
            snippet = result.select_one('.GI74Re.nDgy9d').text
            date_published = result.select_one('.ZE0LJd span').text
            print(f'{title}\n{link}\n{snippet}\n{date_published}\n{source}\n')
            data.append((title, link, snippet, source, date_published))
            dataray = np.asarray(data)
            df = pd.DataFrame(dataray)
            df.columns = ['title', 'link', 'snippet', 'source', 'date']
            df.to_csv(fr'C:\Users\Owner\Desktop\news_scrapR\crp00.csv')
scrape()
