# Inventory Idempotency Solution

This project applies a batch of inventory adjustments to a SQLite database in
a way that's safe to retry: applying the same batch twice never double-counts
an adjustment.

## Setup

From the `solution` directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode:

```bash
pip install -e .
```

## Run the batch processor

```bash
python3 run.py
```

This deletes any existing `warehouse.db` and starts fresh, then applies the
sample batch of adjustments twice in a row to demonstrate idempotency:

```text
Applying batch (first run)...
  applied: 3, skipped: 0
  WIDGET-A: 7
  WIDGET-B: 25

Applying the SAME batch again (e.g. a retry after a timeout)...
  applied: 0, skipped: 3
  WIDGET-A: 7
  WIDGET-B: 25
```

The second run - simulating a retry after a timeout - applies nothing new:
every adjustment is skipped and the quantities are unchanged.

## How idempotency is enforced

`inventory.db.get_connection` (`src/inventory/db.py`) creates a
`processed_events` table with `adjustment_id` as its `PRIMARY KEY`, alongside
the `inventory` table that holds running quantities.

`apply_adjustment` (`src/inventory/processor.py`) records the adjustment with
`INSERT ... ON CONFLICT(adjustment_id) DO NOTHING` *before* touching
inventory. If the adjustment was already recorded, the insert is a no-op
(`cursor.rowcount == 0`) and the function returns `False` without applying
the delta again. This check-and-record happens as one atomic database
operation, so there's no gap between "has this been seen before?" and
"record that it has" for a concurrent or retried call to slip into - the
`PRIMARY KEY` constraint is what actually prevents the duplicate, not
application-level logic.

## Run the tests

```bash
pip install pytest
python3 -m pytest tests/ -v
```

`tests/test_idempotency.py` applies the same batch twice against an
in-memory database and asserts the resulting quantities are identical, and
that the second run reports everything as skipped rather than re-applied.

## Type-check with mypy

```bash
pip install mypy
python3 -m mypy --strict src/inventory run.py tests
```

This should report `Success: no issues found in 6 source files`.

## Troubleshooting

If you see `ModuleNotFoundError: No module named 'inventory'`, make sure you
are using the project virtual environment and have installed the package
with:

```bash
source .venv/bin/activate
pip install -e .
```
