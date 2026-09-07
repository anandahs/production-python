from fxrates.fx_client import fetch_rate    
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


