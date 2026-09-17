import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .driver import get_driver
from .parser import parse_product_card
import config


def scrape_query(query, driver):
    all_results = []

    for page in range(1, config.MAX_PAGES_PER_QUERY + 1):
        url = f"{config.BASE_DOMAIN}/catalog/?q={query.replace(' ', '+')}&page={page}"
        logging.info(f"Scraping: {url}")

        try:
            driver.get(url)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-qa-locator='product-item']")
                )
            )
        except Exception as e:
            logging.warning(f"Page {page} for '{query}' failed to load: {e}")
            break

        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(1)

        cards = driver.find_elements(By.CSS_SELECTOR, "div[data-qa-locator='product-item']")
        if not cards:
            logging.info(f"No more products found for '{query}' at page {page}, stopping.")
            break

        for card in cards[: config.MAX_PRODUCTS_PER_PAGE]:
            data = parse_product_card(card)
            data["search_query"] = query
            data["page"] = page
            all_results.append(data)

        time.sleep(config.REQUEST_DELAY)

    return all_results


def run_all():
    driver = get_driver(headless=config.HEADLESS)
    results_by_query = {}

    try:
        for query in config.SEARCH_QUERIES:
            logging.info(f"Starting query: {query}")
            results = scrape_query(query, driver)
            results_by_query[query] = results
            time.sleep(config.QUERY_DELAY)
    finally:
        driver.quit()

    return results_by_query