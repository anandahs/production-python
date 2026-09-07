import run


def test_failed_historical_rate_lookup_is_recorded_in_dead_letter_queue() -> None:
    results, dead_letter = run.run_billing_job()

    identifier = "USD/XXX@2026-01-02"
    identifiers = [entry["identifier"] for entry in dead_letter.entries]

    assert identifier in identifiers
    entry = next(e for e in dead_letter.entries if e["identifier"] == identifier)
    assert entry["reason"] == "USD/XXX is not a recognized currency pair"

    # A dead-lettered lookup should not also show up as a successful result.
    assert identifier not in results
