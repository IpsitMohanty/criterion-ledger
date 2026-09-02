"""
Criterion Channel — All Films scraper
--------------------------------------
Mechanism confirmed: films.criterionchannel.com renders its entire film
catalog (~3265 entries) server-side, embedded directly in the initial
HTML response, as a plain HTML <table id="gridview">. No pagination,
no lazy-load API, no JS execution needed. A single GET request returns
everything.

Confirmed markup (via view-source):
  <table id="gridview" class="criterion-channel__gridview">
    <tbody class="criterion-channel__tbody" data-is-load-more-container>
      <tr class="criterion-channel__tr" data-role="grid-film"
          data-href="https://www.criterionchannel.com/2-or-3-things-i-know-about-her">
        <td class="criterion-channel__td criterion-channel__td--img">...</td>
        <td class="criterion-channel__td criterion-channel__td--title">
          <a href="...">2 or 3 Things I Know About Her</a>
        </td>
        <td class="criterion-channel__td criterion-channel__td--director">
          Jean-Luc Godard
        </td>
        <td class="criterion-channel__td criterion-channel__td--country">
          France
        </td>
        <td class="criterion-channel__td criterion-channel__td--year">
          1967
        </td>
      </tr>
      ...
"""

import requests
from bs4 import BeautifulSoup
import json
import csv

URL = "https://films.criterionchannel.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}


def fetch_page(url=URL):
    """Single GET request — no pagination or scrolling needed."""
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    resp.encoding = "utf-8"  # avoid the mojibake issue we hit earlier
    return resp.text


def parse_films(html):
    soup = BeautifulSoup(html, "html.parser")
    films = []

    rows = soup.select("table#gridview tbody tr.criterion-channel__tr")

    for row in rows:
        title_tag = row.select_one("td.criterion-channel__td--title a")
        director_td = row.select_one("td.criterion-channel__td--director")
        country_td = row.select_one("td.criterion-channel__td--country")
        year_td = row.select_one("td.criterion-channel__td--year")

        films.append({
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "url": title_tag["href"] if title_tag and title_tag.has_attr("href") else row.get("data-href"),
            "director": director_td.get_text(strip=True) if director_td else None,
            "country": country_td.get_text(strip=True) if country_td else None,
            "year": year_td.get_text(strip=True) if year_td else None,
        })

    return films


def save(films, json_path="criterion_films.json", csv_path="criterion_films.csv"):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(films, f, ensure_ascii=False, indent=2)

    if films:
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=films[0].keys())
            writer.writeheader()
            writer.writerows(films)

    print(f"Saved {len(films)} films to {json_path} and {csv_path}")


if __name__ == "__main__":
    html = fetch_page()
    films = parse_films(html)
    save(films)
