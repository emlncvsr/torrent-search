import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://nyaa.si"
SEARCH_URL = BASE_URL + "/?f=0&c=0_0&q={}&p={}"

def fetch_page(query, page):
    url = SEARCH_URL.format(query, page)
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    torrents = []
    rows = soup.select('table.torrent-list tr.default, tr.success')

    for row in rows:
        title = row.select_one('td:nth-of-type(2) a:not([title="Torrent file"])').text.strip()
        category = row.select_one('td:nth-of-type(1) a').get('title')
        magnet = row.select_one('td:nth-of-type(3) a[href^="magnet"]').get('href')
        size = row.select_one('td:nth-of-type(4)').text.strip()
        date = row.select_one('td:nth-of-type(5)').text.strip()
        seeders = row.select_one('td:nth-of-type(6)').text.strip()
        leechers = row.select_one('td:nth-of-type(7)').text.strip()
        completed = row.select_one('td:nth-of-type(8)').text.strip()

        torrents.append({
            'Title': title,
            'Category': category,
            'Magnet': magnet,
            'Size': size,
            'Date': date,
            'Seeders': seeders,
            'Leechers': leechers,
            'Completed': completed
        })

    return torrents

def save_to_csv(torrents, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=torrents[0].keys())
        writer.writeheader()
        writer.writerows(torrents)

def main(query, max_pages):
    all_torrents = []
    for page in range(1, max_pages + 1):
        html = fetch_page(query, page)
        torrents = parse_page(html)
        all_torrents.extend(torrents)

    save_to_csv(all_torrents, f"{query.replace(' ', '_')}.csv")

if __name__ == "__main__":
    query = input("Enter search query: ")
    max_pages = int(input("Enter number of pages to scrape: "))
    main(query, max_pages)
