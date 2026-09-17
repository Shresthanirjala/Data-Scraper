import os
import logging
import pandas as pd

import config
from scraper.scrape import run_all


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename=config.LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.getLogger().addHandler(logging.StreamHandler())  # also print to console


def main():
    setup_logging()
    os.makedirs(config.RAW_DIR, exist_ok=True)
    os.makedirs(config.PROCESSED_DIR, exist_ok=True)

    results_by_query = run_all()

    all_data = []
    for query, results in results_by_query.items():
        if not results:
            continue
        df = pd.DataFrame(results)
        safe_name = query.replace(" ", "_")
        raw_path = os.path.join(config.RAW_DIR, f"{safe_name}.csv")
        df.to_csv(raw_path, index=False)
        logging.info(f"Saved {len(df)} rows to {raw_path}")
        all_data.append(df)

    if all_data:
        merged = pd.concat(all_data, ignore_index=True)
        merged.drop_duplicates(subset=["link"], inplace=True)
        processed_path = os.path.join(config.PROCESSED_DIR, "all_products.csv")
        merged.to_csv(processed_path, index=False)
        logging.info(f"Saved merged dataset ({len(merged)} rows) to {processed_path}")


if __name__ == "__main__":
    main()