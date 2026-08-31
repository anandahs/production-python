"""Same computations as the starter code. Compare this line by line to
starter/signup_processor.py - the actual logic (how a trial end date
gets computed, how counts get totaled) is unchanged. What changed is
what these functions trust: a validated SignupRecord, not a raw dict
that might contain anything.
"""

from datetime import date, timedelta

from signupflow.models import SignupRecord


def compute_trial_end_dates(records: list[SignupRecord]) -> list[dict[str, str]]:
    results = []
    for record in records:
        trial_end = record.signup_date + timedelta(days=record.trial_days)
        results.append(
            {
                "email": record.email,
                "plan": record.plan,
                "trial_end": trial_end.isoformat(),
            }
        )
    return results


def count_by_plan(records: list[SignupRecord]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        counts[record.plan] = counts.get(record.plan, 0) + 1
    return counts
