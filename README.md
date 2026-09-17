# Daraz Product Data Scraper

A Selenium-based scraper for collecting product listings from Daraz Nepal search results.

## What It Does

When you run the project, it:

1. Opens Daraz Nepal in a Chrome browser controlled by Selenium.
2. Searches for these terms:
   - `laptop`
   - `mobile phone`
   - `headphones`
   - `smart watch`
3. Scrapes up to 3 result pages for each search term.
4. Collects up to 40 product cards per page.
5. Extracts the following fields from each product card:
   - product name
   - price
   - rating
   - product link
   - image URL
   - search query used
   - result page number
6. Saves each search query's results as a separate CSV file in `data/raw/`.
7. Combines all scraped results into one dataset, removes duplicate products using the product link, and saves it as `data/processed/all_products.csv`.
8. Writes detailed progress and warning messages to `logs/scraper.log` and also prints them in the terminal.

The scraper uses a two-second delay between pages and a five-second delay between search terms. These delays are defined in `config.py`.

## Project Structure

```text
.
├── config.py                 # Search terms, limits, delays, and paths
├── main.py                   # Application entry point and CSV output logic
├── requirements.txt          # Python dependencies
├── scraper/
│   ├── driver.py             # Selenium Chrome WebDriver setup
│   ├── parser.py             # Product-card field extraction
│   └── scrape.py             # Search-page scraping workflow
├── data/
│   ├── raw/                  # One CSV file per search query
│   └── processed/            # Combined, de-duplicated dataset
└── logs/                     # Scraper logs
```

## Requirements

- Python 3.9 or newer
- Google Chrome installed
- Internet access
- A working Chrome installation that `webdriver-manager` can use to download the matching ChromeDriver

## Installation

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On Windows, PowerShell may require an execution-policy change before activating the environment. You can also run the Python executable directly from `.venv` without activating it.

## Running the Scraper

From the project root, run:

```powershell
python main.py
```

The program runs in headless Chrome mode by default, so no visible browser window is opened. The first run may take longer because `webdriver-manager` downloads the required ChromeDriver.

## Output Files

For the current configuration, the scraper creates or updates:

```text
data/raw/laptop.csv
data/raw/mobile_phone.csv
data/raw/headphones.csv
data/raw/smart_watch.csv
data/processed/all_products.csv
logs/scraper.log
```

Each raw and processed CSV contains these columns:

```text
name,price,rating,link,image_url,search_query,page
```

A product's `name`, `price`, `rating`, `link`, or `image_url` can be empty when Daraz does not expose that element in the product card. If no rating is found, the parser stores `No rating`.

## Configuration

Edit `config.py` to change the scraper behavior:

```python
SEARCH_QUERIES = ["laptop", "mobile phone", "headphones", "smart watch"]
MAX_PAGES_PER_QUERY = 3
MAX_PRODUCTS_PER_PAGE = 40
HEADLESS = True
REQUEST_DELAY = 2
QUERY_DELAY = 5
```

You can also change the output directories and log file through `RAW_DIR`, `PROCESSED_DIR`, and `LOG_FILE`.

## Important Notes

- The scraper depends on Daraz's current HTML structure and CSS selectors. If Daraz changes its page markup, product extraction may stop working or some fields may become empty.
- The scraper stops a query when a page fails to load or no product cards are found.
- Duplicate products are removed only in `all_products.csv`, using the `link` column. The raw query files retain the results collected for their individual searches.
- The project currently has no automated test suite.
- `beautifulsoup4` is listed as a dependency but is not currently used by the implementation.
- Use the scraper responsibly and respect Daraz's terms of service, robots policy, and applicable laws.
