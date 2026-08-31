from pathlib import Path
from signupflow.loader import load_signup_records
from signupflow.processor import compute_trial_end_dates, count_by_plan

records = load_signup_records(Path("sample_signups.json"))

print("Signup counts by plan:", count_by_plan(records))
print("Trial end dates:", compute_trial_end_dates(records))