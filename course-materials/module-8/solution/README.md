# Reportsvc — Module 8 Solution

A quarterly report generator with typed, validated, fail-fast configuration
via [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

The point of this example: `host` has a safe default (`localhost`), but
`password` has none. That means a missing password fails immediately, with a
clear validation error, the instant `ReportServiceSettings()` is
instantiated — instead of silently connecting to the wrong environment and
returning quietly wrong numbers (see the comments in
[report_db.py](src/reportsvc/report_db.py) for what that looks like).

## Setup

From this directory (`course-materials/module-8/solution`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e .
```

For type checking, also install mypy:

```bash
pip3 install mypy
```

## Configuration

Settings are read from environment variables prefixed with `REPORT_DB_`:

| Env var               | Required | Default     |
|------------------------|----------|-------------|
| `REPORT_DB_HOST`       | No       | `localhost` |
| `REPORT_DB_PASSWORD`   | Yes      | *(none)*    |

## Run

Running without a password fails fast with a validation error:

```bash
python3 run.py
```

Provide the password via environment variable to connect successfully:

```bash
REPORT_DB_PASSWORD="vault-injected-prod-secret-9f3a" python3 run.py
```

(This is the simulated "correct" password baked into
[report_db.py](src/reportsvc/report_db.py) for demo purposes — a real
service would source this from a secrets manager, not a hardcoded value.)
Any other password value "succeeds" but silently returns different,
smaller totals, simulating a connection that landed on the wrong
environment.

## Beyond environment variables: secrets managers

This example reads `password` from a plain environment variable, but
`pydantic-settings` isn't limited to that. It has built-in support for
loading settings straight from real secrets backends instead of `.env`
files or shell exports, including:

- **Docker/Kubernetes secrets** — via `secrets_dir` in `SettingsConfigDict`,
  which reads each field from a file (e.g. `/run/secrets/password`) rather
  than an env var, matching how container orchestrators mount secrets.
- **AWS Secrets Manager** and **Azure Key Vault** — via the optional
  `pydantic-settings[aws-secrets-manager]` / `[azure-key-vault]` extras,
  which provide settings sources that fetch values from those services.
- **Custom secret sources** — by subclassing `PydanticBaseSettingsSource` and
  adding it to `settings_customise_sources`, e.g. to pull from HashiCorp
  Vault or another internal secrets store.

The key idea stays the same as in this example: `password` (or any secret
field) remains a required, typed field with no default, so a
misconfigured or missing secret still fails fast at startup — only *where*
the value comes from changes.

## Type check

```bash
python3 -m mypy src/reportsvc
```

## Project layout

- `run.py` — entry point; loads settings and prints the quarterly report.
- `src/reportsvc/config.py` — `ReportServiceSettings`, the typed,
  environment-aware config with a required `password` field.
- `src/reportsvc/report_db.py` — simulated report database (not meant to be
  edited); returns real totals only for the correct password, otherwise
  quietly wrong ones.
