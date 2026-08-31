from datetime import date
from typing import Literal

from pydantic import BaseModel, model_validator


class SignupRecord(BaseModel):
    email: str
    plan: Literal["free", "pro", "enterprise"]
    signup_date: date
    trial_days: int = 14
    referral_code: str | None = None
    referral_bonus_percent: float | None = None

    @model_validator(mode="after")
    def validate_referral_bonus(self) -> "SignupRecord":
        has_referral = self.referral_code is not None
        bonus = self.referral_bonus_percent

        if has_referral:
            if bonus is None:
                raise ValueError("referral_bonus_percent must be provided when referral_code is set")
            bonus_value = float(bonus)
            if bonus_value < 0 or bonus_value > 100:
                raise ValueError("referral_bonus_percent must be between 0 and 100")
        elif bonus is not None:
            raise ValueError("referral_bonus_percent cannot be provided when referral_code is not set")

        return self



