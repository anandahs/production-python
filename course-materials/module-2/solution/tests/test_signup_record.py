import pytest
from pydantic import ValidationError

from signupflow.models import SignupRecord


def test_signup_record_referral_bonus_validation_valid_and_invalid():
    valid_min = SignupRecord(
        email="customer@example.com",
        plan="pro",
        signup_date="2026-08-01",
        referral_code="SAVE10",
        referral_bonus_percent=0,
    )
    valid_max = SignupRecord(
        email="customer2@example.com",
        plan="enterprise",
        signup_date="2026-08-02",
        referral_code="SAVE100",
        referral_bonus_percent=100,
    )

    assert valid_min.referral_bonus_percent == 0
    assert valid_max.referral_bonus_percent == 100

    with pytest.raises(
        ValidationError,
        match="referral_bonus_percent must be provided when referral_code is set",
    ):
        SignupRecord(
            email="customer@example.com",
            plan="pro",
            signup_date="2026-08-01",
            referral_code="SAVE10",
        )

    with pytest.raises(
        ValidationError,
        match="referral_bonus_percent must be between 0 and 100",
    ):
        SignupRecord(
            email="customer@example.com",
            plan="pro",
            signup_date="2026-08-01",
            referral_code="SAVE10",
            referral_bonus_percent=-1,
        )

    with pytest.raises(
        ValidationError,
        match="referral_bonus_percent must be between 0 and 100",
    ):
        SignupRecord(
            email="customer@example.com",
            plan="pro",
            signup_date="2026-08-01",
            referral_code="SAVE10",
            referral_bonus_percent=101,
        )

    with pytest.raises(
        ValidationError,
        match="referral_bonus_percent cannot be provided when referral_code is not set",
    ):
        SignupRecord(
            email="customer@example.com",
            plan="pro",
            signup_date="2026-08-01",
            referral_bonus_percent=10,
        )
