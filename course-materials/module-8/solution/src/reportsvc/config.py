"""Typed, validated, environment-aware config.

Notice which fields have a default and which don't. `host` has a safe
default - if it's missing, localhost is a genuinely reasonable guess
for local development. `password` has no default at all. That's the
entire fix: a required secret with no fallback means a missing value
raises an error the instant this class gets instantiated, not some
number of hours into quietly running with the wrong one.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class ReportServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REPORT_DB_")

    host: str = "localhost"
    password: str
