from selenium.webdriver.common.by import By


def parse_product_card(card):
    def safe_get(selector, attr=None):
        try:
            el = card.find_element(By.CSS_SELECTOR, selector)
            return el.get_attribute(attr) if attr else el.text
        except Exception:
            return None

    name = safe_get("div[title]", "title")
    price = safe_get("span.currency, span[class*='price']")
    rating = safe_get("span[class*='rating']") or "No rating"
    link = safe_get("a", "href")
    if link and link.startswith("//"):
        link = "https:" + link
    image = safe_get("img", "src")

    return {
        "name": name,
        "price": price,
        "rating": rating,
        "link": link,
        "image_url": image,
    }