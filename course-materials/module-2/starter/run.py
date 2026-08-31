import json

from signup_processor import compute_trial_end_dates, count_by_plan

with open("sample_signups.json") as f:
    records = json.load(f)

print("Signup counts by plan:", count_by_plan(records))
print("Trial end dates:", compute_trial_end_dates(records))
