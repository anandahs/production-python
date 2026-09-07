# FX Rates Solution

This project fetches FX rates for a list of currency pairs, classifying and
retrying transient failures, and routing permanent failures to a dead-letter
queue.

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

## Run the billing job

```bash
python run.py
```

Example output:

```text
Fetching USD/EUR...
  attempt 1 failed: Timed out fetching USD/EUR (attempt 1). Retrying in 0.027 seconds...
  ok: USD/EUR = 0.92
Fetching USD/GBP...
  ok: USD/GBP = 0.79
Fetching USD/XXX...
 dead lettered: USD/XXX - USD/XXX is not a recognized currency pair
Fetching USD/INR...
  ok: USD/INR = 83.1

Fetched 3 rate(s) successfully:
1 pair(s) were sent to dead letter queue:
 - USD/XXX: USD/XXX is not a recognized currency pair
```

Timeouts and service-unavailable errors are retried automatically; a
transient failure that exhausts its retries, or a permanent error such as an
unrecognized pair, is sent to the dead-letter queue instead of failing the run.

## Classified exceptions

`fxrates.exceptions` distinguishes errors by whether retrying can help:

- `RateServiceTimeout` and `RateServiceUnavailable` are **transient** - the
  service didn't respond in time, or is briefly down. Retrying can succeed.
- `InvalidCurrencyPairError` is **permanent** - the pair doesn't exist, so no
  number of retries will ever fix it.

Both are subclasses of `RateServiceError`. `retry.py` only retries the two
transient types (`RETRYABLE_EXCEPTIONS`); a permanent error propagates
immediately to `run.py`, which sends it straight to the dead-letter queue
instead of wasting attempts on a request that can never succeed.

## Backoff and jitter

`call_with_retry` (`fxrates/retry.py`) retries a failed call up to
`max_attempts` times (default 5), using exponential backoff capped at
`max_delay`:

```
backoff = min(base_delay * 2 ** (attempt - 1), max_delay)
delay   = random.uniform(0, backoff)
```

- **Exponential backoff** doubles the wait after each failed attempt
  (`base_delay`, `2 * base_delay`, `4 * base_delay`, ...), so a persistent
  outage isn't hammered at a constant rate. It's capped at `max_delay` so the
  wait doesn't grow unbounded.
- **Jitter** picks the actual delay randomly between `0` and that backoff
  ceiling, rather than sleeping the full amount every time. Without jitter,
  many callers that failed at the same moment would all retry at the same
  moment again (a "thundering herd"); jitter spreads their retries out.

If the call still fails after `max_attempts`, the original exception is
re-raised, which is what allows `run.py` to catch it and dead-letter the pair.

## Type-check with mypy

Install mypy and run it in strict mode against the package and entry point:

```bash
pip install mypy
python3 -m mypy --strict src/fxrates run.py
```

This should report `Success: no issues found in 7 source files`.

## Troubleshooting

If you see `ModuleNotFoundError: No module named 'fxrates'`, make sure you are
using the project virtual environment and have installed the package with:

```bash
source .venv/bin/activate
pip install -e .
```
