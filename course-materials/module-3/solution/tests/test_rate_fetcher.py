import pytest

from fxrates import fx_client
from fxrates.exceptions import InvalidCurrencyPairError, RateServiceTimeout, RateServiceUnavailable
from fxrates.rate_fetcher import get_historical_rate


def test_get_historical_rate_succeeds_immediately_for_non_flaky_pair() -> None:
    fx_client.reset()

    # USD/INR never fails, so retry protection shouldn't kick in at all -
    # it should be a single call.
    rate = get_historical_rate("USD/INR", "2026-01-02")

    assert rate == 83.1
    assert fx_client._call_counts["USD/INR@2026-01-02"] == 1


def test_fetch_historical_rate_raises_transient_exceptions_directly() -> None:
    fx_client.reset()

    # Without the retry wrapper, the flaky service raises its classified
    # transient exceptions on the first attempt(s), same as fetch_rate does.
    with pytest.raises(RateServiceTimeout):
        fx_client.fetch_historical_rate("USD/EUR", "2026-01-02")

    with pytest.raises(RateServiceUnavailable):
        fx_client.fetch_historical_rate("USD/GBP", "2026-01-02")


def test_get_historical_rate_retries_transient_failures_then_succeeds() -> None:
    fx_client.reset()

    # USD/EUR times out on its first two calls, whatever the date - the
    # retry protection in get_historical_rate should absorb that.
    rate = get_historical_rate("USD/EUR", "2026-01-02")

    assert rate == 0.92
    assert fx_client._call_counts["USD/EUR@2026-01-02"] == 3


def test_get_historical_rate_does_not_retry_permanent_errors() -> None:
    fx_client.reset()

    with pytest.raises(InvalidCurrencyPairError):
        get_historical_rate("USD/XXX", "2026-01-02")

    # A permanent error should fail on the first attempt, not be retried.
    assert fx_client._call_counts["USD/XXX@2026-01-02"] == 1


def test_get_historical_rate_tracks_flakiness_independently_per_date() -> None:
    fx_client.reset()

    # Exhaust the flaky attempts for one date...
    get_historical_rate("USD/EUR", "2026-01-01")
    # ...a different date for the same pair should start its own sequence
    # of failures, and still succeed thanks to retry protection.
    rate = get_historical_rate("USD/EUR", "2026-01-02")

    assert rate == 0.92
    assert fx_client._call_counts["USD/EUR@2026-01-01"] == 3
    assert fx_client._call_counts["USD/EUR@2026-01-02"] == 3
