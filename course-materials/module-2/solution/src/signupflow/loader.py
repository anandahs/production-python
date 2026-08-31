"""Where raw, untrusted data enters this codebase, and gets checked
exactly once, before anything downstream ever sees it.
"""

import json
from pathlib import Path

from pydantic import ValidationError

from signupflow.models import SignupRecord


def load_signup_records(path: Path) -> list[SignupRecord]:
    with open(path) as f:
        raw_records = json.load(f)

    validated: list[SignupRecord] = []
    for index, raw in enumerate(raw_records):
        try:
            validated.append(SignupRecord(**raw))
        except ValidationError as e:
            raise ValueError(
                f"Record at index {index} is invalid: {e}\nRaw record: {raw}"
            ) from e

    return validated
