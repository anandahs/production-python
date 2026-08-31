"""The data boundary for signup records.

A raw signup record arrives as an untyped dict - from a webhook, a CSV,
an API response, it doesn't matter. Before any of that data is trusted
anywhere else in this codebase, it passes through this one model. If a
record is malformed, it fails right here, with a specific error naming
the exact field that's wrong - not three functions later, in a place
that has nothing to do with where the bad data actually came from.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel


class SignupRecord(BaseModel):
    email: str
    plan: Literal["free", "pro", "enterprise"]
    signup_date: date
    trial_days: int = 14
    referral_code: str | None = None
