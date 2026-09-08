# Coupon Redemption Solution

This project redeems coupon codes against orders, applying a percentage
discount while enforcing that each coupon code can only ever be used once -
backed by a layered test suite (unit, integration, property-based, and
failure-path tests).

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

## Install test and type-check dependencies

```bash
pip install mypy pytest hypothesis
```

## Run the tests

```bash
python3 -m pytest tests -v
```

Expected output:

```text
tests/test_failure_paths.py::test_unknown_code_raises_invalid_coupon_error PASSED
tests/test_failure_paths.py::test_expired_coupon_raises_expired_coupon_error PASSED
tests/test_failure_paths.py::test_order_below_minimum_raises_minimum_order_not_met_error PASSED
tests/test_failure_paths.py::test_order_exactly_at_minimum_is_accepted PASSED
tests/test_integration_redemption.py::test_same_code_cannot_be_used_by_two_different_orders PASSED
tests/test_integration_redemption.py::test_same_order_can_use_different_codes PASSED
tests/test_property_based.py::test_discounted_total_is_always_between_zero_and_original PASSED
tests/test_unit_calculation.py::test_applies_percentage_discount PASSED
tests/test_unit_calculation.py::test_zero_discount_leaves_total_unchanged PASSED
tests/test_unit_calculation.py::test_full_discount_gives_zero PASSED
tests/test_unit_calculation.py::test_rounds_to_two_decimal_places PASSED

11 passed
```

### What each layer of the suite is checking

- **`test_unit_calculation.py`** - `compute_discounted_total` against a few
  hand-picked percentages (0%, 100%, rounding).
- **`test_failure_paths.py`** - each of `InvalidCouponError`,
  `ExpiredCouponError`, and `MinimumOrderNotMetError` is actually raised for
  an unknown code, an expired coupon, and an order below the minimum.
- **`test_integration_redemption.py`** - runs against a real (in-memory)
  SQLite database rather than a mock. This is what actually catches the bug
  this module is built around: the `UNIQUE`/`PRIMARY KEY` constraint in
  `src/discounts/db.py` is on `code`, not `order_id`, so a given coupon code
  can only ever be redeemed once, while a single order can legitimately use
  several different codes.
- **`test_property_based.py`** - uses `hypothesis` to generate hundreds of
  `(order_total, discount_percent)` pairs and asserts the invariant that a
  discounted total is always between `0` and the original order total,
  instead of checking only a few hand-picked numbers.

## Type-check with mypy

```bash
python3 -m mypy --strict src/discounts tests
```

This should report `Success: no issues found in 8 source files`.

## Troubleshooting

If you see `ModuleNotFoundError: No module named 'discounts'`, make sure you
are using the project virtual environment and have installed the package
with:

```bash
source .venv/bin/activate
pip install -e .
```

If you see `No module named pytest` (or `hypothesis`/`mypy`), install the
dependencies above inside the activated virtual environment.
