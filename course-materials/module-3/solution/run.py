from fxrates.fx_client import reset
from fxrates.rate_fetcher import get_historical_rate, get_rate
from fxrates.dead_letter import DeadLetter
from fxrates.exceptions import RateServiceError

PAIRS_NEEDED_FOR_TODAYS_BILLING_RUN = ["USD/EUR", "USD/GBP", "USD/XXX", "USD/INR"]

HISTORICAL_RATES_NEEDED_FOR_TODAYS_BILLING_RUN: list[tuple[str, str]] = [
    ("USD/EUR", "2026-01-02"),
    ("USD/GBP", "2026-01-02"),
    ("USD/XXX", "2026-01-02"),
    ("USD/INR", "2026-01-02"),
]


def run_billing_job() -> tuple[dict[str, float], DeadLetter]:
    reset()
    dead_letter = DeadLetter()
    results: dict[str, float] = {}

    for pair in PAIRS_NEEDED_FOR_TODAYS_BILLING_RUN:
        print(f"Fetching {pair}...")
        try:
            rate = get_rate(pair)
            results[pair] = rate
            print(f"  ok: {pair} = {rate}")
        except RateServiceError as e:
            dead_letter.add(pair, str(e))
            print(f" dead lettered: {pair} - {e}")

    for pair, date in HISTORICAL_RATES_NEEDED_FOR_TODAYS_BILLING_RUN:
        identifier = f"{pair}@{date}"
        print(f"Fetching historical {identifier}...")
        try:
            rate = get_historical_rate(pair, date)
            results[identifier] = rate
            print(f"  ok: {identifier} = {rate}")
        except RateServiceError as e:
            dead_letter.add(identifier, str(e))
            print(f" dead lettered: {identifier} - {e}")

    return results, dead_letter


def main() -> None:
    results, dead_letter = run_billing_job()

    print("")
    print(f"Fetched {len(results)} rate(s) successfully:")
    print(f"{len(dead_letter)} pair(s) were sent to dead letter queue:")

    for entry in dead_letter.entries:
        print(f" - {entry['identifier']}: {entry['reason']}")

if __name__ == "__main__":
    main()