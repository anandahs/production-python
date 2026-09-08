"""Proves idempotency the way the capstone spec asks for: a test that
runs the same operation twice and asserts the end state is identical,
not a test that just checks nothing crashed.
"""

from inventory.db import get_connection, get_quantity
from inventory.processor import Adjustment, apply_batch

ADJUSTMENTS: list[Adjustment] = [
    {"adjustment_id": "adj-100", "sku": "WIDGET-C", "quantity_delta": 5},
    {"adjustment_id": "adj-101", "sku": "WIDGET-C", "quantity_delta": 20},
]


def test_applying_the_same_batch_twice_gives_the_same_result() -> None:
    conn = get_connection(":memory:")

    first_result = apply_batch(conn, ADJUSTMENTS)
    quantity_after_first_run = get_quantity(conn, "WIDGET-C")

    second_result = apply_batch(conn, ADJUSTMENTS)
    quantity_after_second_run = get_quantity(conn, "WIDGET-C")

    # The actual proof: running it twice changed nothing extra.
    assert quantity_after_first_run == quantity_after_second_run == 25

    # And the second run should show it correctly skipped everything,
    # not silently re-applied it.
    assert first_result == {"applied": 2, "skipped": 0}
    assert second_result == {"applied": 0, "skipped": 2}
