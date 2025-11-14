from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "ecommerce.db"


QUERY = """
SELECT
    u.first_name || ' ' || u.last_name AS user_name,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id
ORDER BY total_spent DESC
LIMIT 5;
"""


def get_top_users_by_spending() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(QUERY)
        results = cursor.fetchall()

    print("Top 5 Users by Total Spending:")
    for name, total in results:
        print(f"{name}: ${total}")


def main() -> None:
    get_top_users_by_spending()


if __name__ == "__main__":
    main()

