# Notifier — Module 6 Solution

An order confirmation notifier with structured, diagnosable logging via
[structlog](https://www.structlog.org/). Every log line is tagged with a
`run_id` for the batch and, where relevant, an `order_id` — but never
`customer_email`, since that's PII and isn't needed to diagnose a delivery
failure.

## Setup

From this directory (`course-materials/module-6/solution`):

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

This processes a batch of sample orders and prints structured JSON log lines
to stdout. One order (`ORD-1003`) is designed to fail deterministically, so
you can see what a failed delivery looks like in the logs.

## Type check

```bash
python3 -m mypy --strict src/notifier
```

## Project layout

- `run.py` — entry point; defines the sample order batch and configures
  structlog.
- `src/notifier/notifier.py` — batch processing and logging logic.
- `src/notifier/email_service.py` — simulated email delivery (not meant to
  be edited; `ORD-1003` always raises to simulate a real failure).
