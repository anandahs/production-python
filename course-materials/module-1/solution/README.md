# Sales Report Solution

This project provides a small CLI for generating a revenue-by-store summary from a CSV file.

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

## Verify the CLI

After installation, confirm the entry point is available:

```bash
salesreport --help
```

## Generate a report

Run the CLI against the sample dataset:

```bash
salesreport generate --input sample_data/sales_sample.csv
```

Example output:

```text
Revenue by store:
  S001: $289.75
  S002: $257.37
  S003: $129.98
```

## Troubleshooting

If you see `ModuleNotFoundError: No module named 'report'`, make sure you are using the project virtual environment and have installed the package with:

```bash
source .venv/bin/activate
pip install -e .
```
