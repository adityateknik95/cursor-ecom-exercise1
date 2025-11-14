from __future__ import annotations

from pathlib import Path
from typing import Dict
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "ecommerce.db"
CSV_FILES: Dict[str, str] = {
    "users": "users.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "reviews": "reviews.csv",
}


def load_csvs_to_sqlite() -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        for table_name, filename in CSV_FILES.items():
            csv_path = BASE_DIR / filename
            if not csv_path.exists():
                raise FileNotFoundError(f"Expected CSV file not found: {csv_path}")

            df = pd.read_csv(csv_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)


def main() -> None:
    load_csvs_to_sqlite()
    print("CSV data ingested into ecommerce.db successfully")


if __name__ == "__main__":
    main()

