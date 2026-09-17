SEARCH_QUERIES = [
    "laptop",
    "mobile phone",
    "headphones",
    "smart watch",
]

MAX_PAGES_PER_QUERY = 3
MAX_PRODUCTS_PER_PAGE = 40
HEADLESS = True
REQUEST_DELAY = 2          # seconds between pages
QUERY_DELAY = 5            # seconds between different search terms
BASE_DOMAIN = "https://www.daraz.com.np"

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
LOG_FILE = "logs/scraper.log"