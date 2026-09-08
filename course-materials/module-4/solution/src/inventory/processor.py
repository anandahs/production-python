import sqlite3
from datetime import datetime, timezone
from typing import TypedDict

from inventory.db import get_quantity


class Adjustment(TypedDict):
    adjustment_id: str
    sku: str
    quantity_delta: int


def apply_adjustment(conn: sqlite3.Connection, adjustment: Adjustment) -> bool:
    """Returns True if this adjustment was actually applied, False if it
    had already been processed before (and was correctly skipped).
    """
    adjustment_id = adjustment["adjustment_id"]

    # This is the whole fix, in one statement. The database either
    # inserts this adjustment_id - meaning we've genuinely never seen it
    # before - or it doesn't, atomically, because the PRIMARY KEY
    # constraint rejects the duplicate. There's no gap between "check if
    # it exists" and "record that it exists" for a second caller to slip
    # into - it's one operation, not two.
    cursor = conn.execute(
        "INSERT INTO processed_events (adjustment_id, processed_at) "
        "VALUES (?, ?) ON CONFLICT(adjustment_id) DO NOTHING",
        (adjustment_id, datetime.now(timezone.utc).isoformat()),
    )

    if cursor.rowcount == 0:
        # Already processed. Applying the delta again would double it -
        # so we don't touch inventory at all, and say so honestly.
        conn.commit()
        return False

    sku = adjustment["sku"]
    current = get_quantity(conn, sku)
    new_quantity = current + adjustment["quantity_delta"]
    conn.execute(
        """
        INSERT INTO inventory (sku, quantity) VALUES (?, ?)
        ON CONFLICT(sku) DO UPDATE SET quantity = ?
        """,
        (sku, new_quantity, new_quantity),
    )
    conn.commit()
    return True


def apply_batch(conn: sqlite3.Connection, adjustments: list[Adjustment]) -> dict[str, int]:
    applied = 0
    skipped = 0
    for adjustment in adjustments:
        if apply_adjustment(conn, adjustment):
            applied += 1
        else:
            skipped += 1
    return {"applied": applied, "skipped": skipped}
