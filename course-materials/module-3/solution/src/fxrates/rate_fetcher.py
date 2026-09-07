from fxrates.fx_client import fetch_historical_rate, fetch_rate
from fxrates.retry import call_with_retry


def get_rate(pair: str) -> float:
    """Fetch the FX rate for the given currency pair, retrying if necessary.

    Args:
        pair: The currency pair to fetch the rate for (e.g., "USD/EUR").

    Returns:
        The FX rate for the given currency pair.

    Raises:
        RuntimeError: If the rate could not be fetched after multiple attempts.
    """
    return call_with_retry(lambda: fetch_rate(pair))


def get_historical_rate(pair: str, date: str) -> float:
    """Fetch the historical FX rate for a currency pair on a given date, retrying if necessary.

    Args:
        pair: The currency pair to fetch the rate for (e.g., "USD/EUR").
        date: The date to fetch the historical rate for (e.g., "2026-01-02").

    Returns:
        The FX rate for the given currency pair on the given date.

    Raises:
        RuntimeError: If the rate could not be fetched after multiple attempts.
    """
    return call_with_retry(lambda: fetch_historical_rate(pair, date))


