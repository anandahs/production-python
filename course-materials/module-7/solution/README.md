# Pricecheck — Module 7 Solution

A bounded-concurrency, chunked price checker. It queries a simulated
third-party pricing API that can only handle a limited number of concurrent
requests, and demonstrates two complementary techniques for working within
that limit:

- **A semaphore** ([price_checker.py](src/pricecheck/price_checker.py)) caps
  how many `fetch_price` calls can be genuinely in flight at once, so the
  real service is never overwhelmed no matter how many SKUs are requested.
- **Chunking** ([catalog.py](src/pricecheck/catalog.py)) processes a large
  catalog in bounded batches so that only one batch's worth of tasks is ever
  created in memory at a time — important once a catalog grows from
  hundreds to hundreds of thousands of SKUs.

## Setup

From this directory (`course-materials/module-7/solution`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e .
```

For type checking, also install mypy:

```bash
pip3 install mypy
```

## Run

```bash
python3 run.py
```

This first prices a small batch of 50 SKUs using `check_all_prices`, then
prices a simulated 500-SKU catalog in chunks of 50 using
`check_full_catalog`, printing timing and progress for each stage.

## Type check

```bash
python3 -m mypy src/pricecheck
```

## Project layout

- `run.py` — entry point; drives both the small-batch and chunked-catalog
  examples.
- `src/pricecheck/pricing_api.py` — simulated third-party pricing service
  (not meant to be edited); rejects requests once more than
  `MAX_CONCURRENT_REQUESTS` (5) are in flight at once.
- `src/pricecheck/price_checker.py` — bounds concurrency with an
  `asyncio.Semaphore` set below the service's real limit.
- `src/pricecheck/catalog.py` — chunks a (potentially huge, lazily
  generated) catalog into fixed-size batches so task creation itself stays
  bounded.
