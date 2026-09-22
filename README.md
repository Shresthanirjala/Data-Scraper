# Daraz Product Data Scraper

A Selenium-based scraper that collects product listings from [Daraz Nepal](https://www.daraz.com.np) search results and exports them as CSV datasets.

## Overview

Running the scraper will:

1. Launch Chrome (headless by default) via Selenium.
2. Search Daraz Nepal for each configured term — by default: `laptop`, `mobile phone`, `headphones`, `smart watch`.
3. Walk up to 3 result pages per search term, scraping up to 40 product cards per page.
4. Pull the following fields from each product card:
   - `name`
   - `price`
   - `rating` (`"No rating"` if none is shown)
   - `link`
   - `image_url`
   - `search_query`
   - `page`
5. Write one CSV per search term to `data/raw/`, then merge everything into a single deduplicated dataset at `data/processed/all_products.csv` (deduplicated by `link`).
6. Log progress and warnings to `logs/scraper.log` and the console.

A 2-second delay is applied between pages and a 5-second delay between search terms to avoid hammering the site; both are configurable.

## Project Layout

```text
.
├── config.py                 # Search terms, limits, delays, paths
├── main.py                   # Entry point: runs the scrape, writes CSVs
├── requirements.txt
├── scraper/
│   ├── driver.py              # Chrome WebDriver setup (headless, UA, options)
│   ├── parser.py               # Extracts fields from a single product card
│   └── scrape.py                # Paginates search results per query
├── data/
│   ├── raw/                    # One CSV per search query
│   └── processed/              # Combined, deduplicated dataset
└── logs/                      # scraper.log
```

## Requirements

- Python 3.9+
- Google Chrome installed
- Internet access (ChromeDriver is fetched automatically via `webdriver-manager` on first run)

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

(If PowerShell blocks activation, adjust the execution policy, or just call the interpreter in `.venv\Scripts\` directly without activating.)

## Usage

```powershell
python main.py
```

Chrome runs headless by default (`HEADLESS = True` in `config.py`), so no window will appear. The first run takes a bit longer while ChromeDriver downloads.

## Output

Given the default configuration, you'll get:

```text
data/raw/laptop.csv
data/raw/mobile_phone.csv
data/raw/headphones.csv
data/raw/smart_watch.csv
data/processed/all_products.csv
logs/scraper.log
```

Every CSV shares the same columns:

```text
name,price,rating,link,image_url,search_query,page
```

Some fields (`name`, `price`, `link`, `image_url`) may come back empty when Daraz's markup doesn't expose that element for a given card.

## Configuration

All tunable behavior lives in `config.py`:

```python
SEARCH_QUERIES = ["laptop", "mobile phone", "headphones", "smart watch"]
MAX_PAGES_PER_QUERY = 3
MAX_PRODUCTS_PER_PAGE = 40
HEADLESS = True
REQUEST_DELAY = 2   # seconds between pages
QUERY_DELAY = 5     # seconds between search terms
```

`RAW_DIR`, `PROCESSED_DIR`, and `LOG_FILE` control where output goes.

## Notes & Caveats

- Extraction relies on Daraz's current HTML/CSS selectors. If their markup changes, fields may come back empty or scraping may fail outright.
- A query stops early if a page fails to load or returns no product cards.
- Deduplication (by `link`) only happens in `all_products.csv` — the per-query raw files keep every result as scraped.
- There's no automated test suite yet.
- `beautifulsoup4` is in `requirements.txt` but unused by the current implementation.
- Please scrape responsibly — respect Daraz's terms of service and robots policy, and don't hit the site harder than necessary.
