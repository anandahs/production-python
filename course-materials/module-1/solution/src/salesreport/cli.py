"""
 Command line entry point for sales report generation.
 This module provides a command line interface (CLI) for generating sales reports from a CSV file.
 It uses the core logic defined in the `report` module to read sales data and calculate total revenue by store.
 The CLI can be executed directly from the command line, and it will print the revenue by store to the console.

"""

from __future__ import annotations

from pathlib import Path

import click

from salesreport.report import read_sales_rows, total_revenue_by_store, validate_rows


@click.group()
def cli() -> None:
    """Sales report command line interface."""


@click.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the sales CSV file containing sales data.",
)
def generate(input_path: Path) -> None:
    """Generate a sales report from the given input CSV file."""
    rows = read_sales_rows(input_path)
    totals = total_revenue_by_store(rows)
    click.echo("Revenue by store:")
    for store, total in sorted(totals.items()):
        click.echo(f"  {store}: ${total:.2f}")


@click.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the sales CSV file containing sales data.",
)
def validate(input_path: Path) -> None:
    """Validate sales rows and print the reasons rows were skipped."""
    rows = read_sales_rows(input_path)
    skipped, reasons = validate_rows(rows)

    click.echo(f"Skipped {skipped} rows")
    for reason, count in sorted(reasons.items()):
        click.echo(f"  {reason}: {count}")

    if skipped == 0:
        click.echo("No invalid rows found.")


cli.add_command(generate)
cli.add_command(validate)

if __name__ == "__main__":
    cli()