"""A small, reusable tool for checking real records from the mock API
against the current IngestionRecord model.

Run this any time the model changes, or any time you want to see how
much of a real page of data currently validates cleanly.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import urllib.request
import json

from pipeline.models import IngestionRecord
from pydantic import ValidationError

with urllib.request.urlopen(
    "http://localhost:8000/records?date=2026-07-01&page=1"
) as r:
    records = json.load(r)["records"]

valid = 0
for rec in records:
    try:
        IngestionRecord(**rec)
        valid += 1
    except ValidationError as e:
        print("Rejected:", e)
        print()

print(f"{valid} of {len(records)} records validated cleanly")