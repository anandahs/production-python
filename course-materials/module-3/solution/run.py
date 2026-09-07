from fxrates.fx_client import reset
from fxrates.rate_fetcher import get_rate
from fxrates.dead_letter import DeadLetter
from fxrates.exceptions import RateServiceError

PAIRS_NEEDED_FOR_TODAYS_BILLING_RUN = ["USD/EUR", "USD/GBP", "USD/XXX", "USD/INR"]

def main() -> None:
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

    print("")
    print(f"Fetched {len(results)} rate(s) successfully:")
    print(f"{len(dead_letter)} pair(s) were sent to dead letter queue:")

    for entry in dead_letter.entries:
        print(f" - {entry['identifier']}: {entry['reason']}")

if __name__ == "__main__":
    main()