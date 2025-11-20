import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE = "http://quotes.toscrape.com"
quotes_list = []

def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.select(".quote")
    for q in quotes:
        text = q.select_one(".text").get_text(strip=True)
        author = q.select_one(".author").get_text(strip=True)
        tags = [t.get_text(strip=True) for t in q.select(".tag")]
        quotes_list.append({
            "text": text,
            "author": author,
            "tags": ",".join(tags)
        })

    next_btn = soup.select_one(".next a")
    return BASE + next_btn["href"] if next_btn else None


def main():
    url = BASE
    page_no = 1

    while url:
        print(f"Scraping page {page_no} … {url}")
        url = parse_page(url)
        page_no += 1
        time.sleep(1)  # polite delay

    df = pd.DataFrame(quotes_list)
    df.to_csv("quotes.csv", index=False)
    print(f"Scraping completed! Saved {len(df)} quotes to quotes.csv")

if __name__ == "__main__":
    main()
