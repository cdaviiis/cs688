"""
CS688 HW 1
1. Use BeautifulSoup and search for three keywords, e.g., (“ChatGPT“ and “Reinforcement Learning”)
or (“Long Covid” and “Booster shot”) and download 50 article titles from the search result via
web scraping. Each record needs to have at least one of the three keywords.
2. Store the downloaded articles’ titles on your local drive in a standard file format, e.g., CSV.
Our script satisfies the criteria above by doing the following:
- Sends GET requests to Bing News search with our query params ("ai", "invest",
"compute")
- pages through results until we have 50 article titles
- writes title content to a CSV file.
"""
import time as t

import requests as r
from bs4 import BeautifulSoup as bs

keywords = ["ai", "invest", "compute"]
query = " ".join(keywords)  # combined query sent to Bing News
base_url = "https://www.bing.com/news/search"
results_needed = 50
page_size = 10  # Bing paginates ~10 results per page
output_csv = "search_results_titles.csv"
headers = {
    # A realistic User-Agent helps avoid being blocked/redirected
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}
titles = []
offset = 0
while len(titles) < results_needed:
    params = {
        "q": query,
        "first": offset,  # pagination offset param used by Bing
    }
    response = r.get(base_url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    soup = bs(response.text, features="html.parser")
    # Bing News result cards use an <a class="title"> element for the headline
    page_titles = []
    for tag in soup.select("a.title"):
        text = tag.get_text(strip=True)
        if text:
            page_titles.append(text)
    for title in page_titles:
        if title not in titles:  # avoid dupe titles being stored
            titles.append(title)
        if len(titles) >= results_needed:
            break
    offset += page_size
    # avoid overwhelming server / rate limited
    t.sleep(1)
titles = titles[:results_needed]
with open(output_csv, "w") as f:
    for title in titles:
        f.write(title + "\n")
