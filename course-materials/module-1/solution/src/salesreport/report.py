""" Core sales-report logic.

This module contains the core logic for reading sales data from a CSV file and calculating total revenue by store. 
It provides two main functions: `read_sales_rows` for reading the sales data into a list of dictionaries,
 and `total_revenue_by_store` for calculating the total revenue for each store based on the sales data.

"""

import csv
from pathlib import Path


def read_sales_rows(path: Path) -> list[dict[str, str]]:
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def total_revenue_by_store(rows: list[dict[str, str]]) -> dict[str, float]:
    totals = {}
    for row in rows:
        store = row["store_id"]
        qty = int(row["quantity"])
        price = float(row["unit_price"])
        totals[store] = totals.get(store, 0.0) + qty * price
    return totals
