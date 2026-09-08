"""Sets up the inventory database - now with a second table.

inventory holds the running counts, same as before. processed_events is
new: a ledger of every adjustment_id that's already been applied, with
a PRIMARY KEY constraint enforcing that each one can only be recorded
once. That constraint is what makes idempotency provable, not just
hoped for - the database itself refuses a duplicate, atomically.
"""

import sqlite3


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            sku TEXT PRIMARY KEY,
            quantity INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS processed_events (
            adjustment_id TEXT PRIMARY KEY,
            processed_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def get_quantity(conn: sqlite3.Connection, sku: str) -> int:
    row = conn.execute("SELECT quantity FROM inventory WHERE sku = ?", (sku,)).fetchone()
    return row[0] if row else 0
