""" Core sales-report logic.

This module contains the core logic for reading sales data from a CSV file and calculating total revenue by store. 
It provides two main functions: `read_sales_rows` for reading the sales data into a list of dictionaries,
 and `total_revenue_by_store` for calculating the total revenue for each store based on the sales data.

"""

import csv
from collections import Counter
from pathlib import Path


def read_sales_rows(path: Path) -> list[dict[str, str]]:
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_rows(rows: list[dict[str, str]]) -> tuple[int, Counter[str]]:
    """Return the number of skipped rows and the reasons they were skipped."""
    skipped = 0
    reasons: Counter[str] = Counter()

    for row in rows:
        if not row.get("store_id"):
            reasons["missing store_id"] += 1
            skipped += 1
            continue

        if not row.get("quantity"):
            reasons["missing quantity"] += 1
            skipped += 1
            continue

        try:
            int(row["quantity"])
        except (TypeError, ValueError):
            reasons["invalid quantity"] += 1
            skipped += 1
            continue

    return skipped, reasons


def total_revenue_by_store(rows: list[dict[str, str]]) -> dict[str, float]:
    totals = {}
    for row in rows:
        store = row["store_id"]
        qty = int(row["quantity"])
        price = float(row["unit_price"])
        totals[store] = totals.get(store, 0.0) + qty * price
    return totals
