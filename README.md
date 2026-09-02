# Criterion Ledger

A personal, offline watch-tracker for the [Criterion Channel](https://www.criterionchannel.com) catalog. Not affiliated with or endorsed by The Criterion Collection — this is an unofficial tool built for personal use.

I built this as a cinephile trying to actually work through a 3,000+ film catalog with some intention — tracking what I've seen, building director retrospectives instead of watching at random, and catching things before they leave the service. If you're in the same boat, feel free to use it too.

Everything runs as a single self-contained HTML file, no server, no build step, no account required. Your watch history stays in your own browser's local storage — nothing is uploaded anywhere.

## What it does

- **Tracker** — search and filter the full film catalog by title, director, country, and year range; mark films as watched.
- **Retrospectives** — browse any director's complete filmography in chronological order, with watch status per film.
- **Random Pick** — draws a random unwatched film, filterable by year range, country, or director.
- **Expiring Watch** — links to Criterion's own official monthly "leaving soon" list (published at the start of each month), with a paste-and-cross-check tool against your own catalog and watch status.
- **Insights** — breakdowns of your watching by decade, country, and director, plus a daily/trend view of your watching pace over time.
- **Export watched films** — download a CSV of everything you've watched (title, director, country, year, date watched), including films that have since been removed from the catalog — your watch history is never lost even if Criterion later pulls a title.

The catalog updates by re-running the included scraper and loading the fresh JSON into the tracker — see below.

## Why the catalog data isn't included

`films.criterionchannel.com` renders its entire film listing server-side in a plain HTML table — no API, no pagination, no JavaScript required to read it. That's confirmed by comparing the page's raw source directly: a single `GET` request returns the full ~3,265-film catalog embedded in the response.

This repo ships **without** that scraped data baked in. You generate your own fresh copy locally and load it into the tracker yourself, rather than this repo redistributing Criterion's catalog listing.

## Setup

1. **Get a fresh catalog snapshot:**
   ```bash
   pip install requests beautifulsoup4
   python scrape_criterion.py
   ```
   This produces `criterion_films.json` and `criterion_films.csv` in the same folder.

2. **Open `criterion_tracker.html`** in any browser.

3. Click **"Update catalog (.json)"** in the header and select the `criterion_films.json` you just generated.

That's it — the tracker saves the catalog and your watch history to your browser's local storage, so it'll still be there next time you open the file (as long as you keep using the same file + browser).

## Keeping it up to date

Criterion's catalog changes over time. Re-run `scrape_criterion.py` whenever you want a refresh (monthly is reasonable), and re-upload via "Update catalog." The tracker will show you exactly what was added and removed since your last snapshot, and log it permanently — newly added titles get a **NEW** tag in the tracker for 45 days.

## How the scraper works

`scrape_criterion.py` makes one plain HTTP GET request to the public catalog page and parses the HTML table with BeautifulSoup — no browser automation, no authentication, no rate-limit concerns beyond normal courteous use (don't run it in a tight loop).

```
table#gridview
  tbody[data-is-load-more-container]
    tr.criterion-channel__tr[data-href="..."]
      td.criterion-channel__td--title > a   → title, url
      td.criterion-channel__td--director    → director
      td.criterion-channel__td--country     → country
      td.criterion-channel__td--year        → year
```

## Notes

- Your watched list is stored per-file, per-browser (via `localStorage` when opened directly as a file, or the platform's own storage API if run inside a compatible AI artifact environment). It won't sync across browsers or machines automatically.
- The site's markup could change in the future, which would require updating the CSS selectors in `scrape_criterion.py`.
- No copyrighted content (video, images, descriptions) is scraped or stored — only structural metadata (title, director, country, year, URL).
