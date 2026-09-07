class IngestionError(Exception):
    """Base class for anything that can go wrong during ingesting a record."""

class UpstreamTimeout(IngestionError):
    """The upstream service didn't respond in time. Transient - retrying can help."""

class UpStreamRateLimited(IngestionError):
    """The API returned 429 . Retryable - after waiting."""

class RecordValidationError(IngestionError):
    """The record is invalid. Not retryable - the data is wrong."""

