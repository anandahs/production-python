import json
from pathlib import Path

from signupflow.models import SignupRecord

from pydantic import ValidationError


def load_signup_records(path: Path) -> list[SignupRecord]:
    with open(path) as f:
        raw_records = json.load(f)

    validated: list[SignupRecord] = []

    for index, raw in enumerate(raw_records):
        try:
            validated.append(SignupRecord(**raw))
        except ValidationError as e:
            raise ValueError(
                f"Record at index {index} is invalid: {e}\n Raw record: {raw}"
                )

    return validated
