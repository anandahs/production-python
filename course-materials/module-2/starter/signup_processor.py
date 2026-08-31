from datetime import date, timedelta


def compute_trial_end_dates(records):
    results = []
    for record in records:
        signup_date = date.fromisoformat(record["signup_date"])
        trial_days = record.get("trial_days", 14)
        trial_end = signup_date + timedelta(days=trial_days)
        results.append(
            {
                "email": record["email"],
                "plan": record["plan"],
                "trial_end": trial_end.isoformat(),
            }
        )
    return results


def count_by_plan(records):
    counts = {}
    for record in records:
        plan = record["plan"]
        counts[plan] = counts.get(plan, 0) + 1
    return counts
