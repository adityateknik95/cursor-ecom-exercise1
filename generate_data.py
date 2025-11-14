from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from random import randint, choice, seed
from typing import List, Dict, Any

import pandas as pd
from faker import Faker


OUTPUT_FILES = {
    "users": "users.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "reviews": "reviews.csv",
}
RECORD_COUNT = 50
DATA_DIR = Path(__file__).parent


def generate_users(fake: Faker) -> List[Dict[str, Any]]:
    users = []
    for user_id in range(1, RECORD_COUNT + 1):
        users.append(
            {
                "user_id": user_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.email(),
                "phone": fake.phone_number(),
                "address": fake.address().replace("\n", ", "),
                "city": fake.city(),
                "country": fake.country(),
                "created_at": fake.date_time_between(start_date="-2y", end_date="now").isoformat(),
            }
        )
    return users


def generate_products(fake: Faker) -> List[Dict[str, Any]]:
    categories = ["Electronics", "Home", "Sports", "Beauty", "Toys", "Books"]
    products = []
    for product_id in range(1, RECORD_COUNT + 1):
        price = round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=5, max_value=500), 2)
        products.append(
            {
                "product_id": product_id,
                "name": fake.catch_phrase(),
                "category": choice(categories),
                "price": price,
                "stock": randint(10, 500),
                "created_at": fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
            }
        )
    return products


def generate_orders(fake: Faker) -> List[Dict[str, Any]]:
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    orders = []
    for order_id in range(1, RECORD_COUNT + 1):
        orders.append(
            {
                "order_id": order_id,
                "user_id": randint(1, RECORD_COUNT),
                "order_date": fake.date_time_between(start_date="-6m", end_date="now").isoformat(),
                "status": choice(statuses),
                "shipping_address": fake.address().replace("\n", ", "),
                "total_amount": 0.0,
            }
        )
    return orders


def generate_order_items(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    order_items = []
    for order_id in range(1, RECORD_COUNT + 1):
        product = choice(products)
        quantity = randint(1, 5)
        subtotal = round(product["price"] * quantity, 2)
        order_items.append(
            {
                "order_item_id": order_id,
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": product["price"],
                "subtotal": subtotal,
            }
        )
    return order_items


def update_order_totals(orders: List[Dict[str, Any]], order_items: List[Dict[str, Any]]) -> None:
    totals = defaultdict(float)
    for item in order_items:
        totals[item["order_id"]] += item["subtotal"]

    for order in orders:
        order["total_amount"] = round(totals[order["order_id"]], 2)


def generate_reviews(fake: Faker) -> List[Dict[str, Any]]:
    reviews = []
    for review_id in range(1, RECORD_COUNT + 1):
        reviews.append(
            {
                "review_id": review_id,
                "user_id": randint(1, RECORD_COUNT),
                "product_id": randint(1, RECORD_COUNT),
                "rating": randint(1, 5),
                "review_text": fake.sentence(nb_words=16),
                "review_date": fake.date_time_between(start_date="-6m", end_date="now").isoformat(),
            }
        )
    return reviews


def write_csv(file_name: str, records: List[Dict[str, Any]]) -> None:
    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / file_name, index=False)


def main() -> None:
    seed(42)
    fake = Faker()
    fake.seed_instance(42)

    users = generate_users(fake)
    products = generate_products(fake)
    orders = generate_orders(fake)
    order_items = generate_order_items(products)
    update_order_totals(orders, order_items)
    reviews = generate_reviews(fake)

    write_csv(OUTPUT_FILES["users"], users)
    write_csv(OUTPUT_FILES["products"], products)
    write_csv(OUTPUT_FILES["orders"], orders)
    write_csv(OUTPUT_FILES["order_items"], order_items)
    write_csv(OUTPUT_FILES["reviews"], reviews)

    print("Data generated successfully")


if __name__ == "__main__":
    main()

