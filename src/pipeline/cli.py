"""Command-line entry point for the ingestion pipeline.

This is a stub for now - it doesn't ingest anything yet. That logic
arrives in later modules. Right now, this file's only job is to prove
the package, the CLI entry point, and the installed command all work
correctly end to end.
"""

import click


@click.group()
def cli() -> None:
    """pipeline - production-grade ingestion and transformation service."""


@cli.command()
@click.option(
    "--date",
    required=True,
    help="Date to ingest records for, in YYYY-MM-DD format.",
)
def ingest(date: str) -> None:
    """Ingest records for a given date. Stub only, for now."""
    click.echo(f"Would ingest records for {date}. Not implemented yet.")


if __name__ == "__main__":
    cli()