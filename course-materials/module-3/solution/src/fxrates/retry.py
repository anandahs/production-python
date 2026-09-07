"""
  A retry helper that only retries what is actually worth retrying.

  The single most important line in this file is the RETRYABLE tuple.
  Everything else - backoff, jitter, max attempts - only matters once you have correctly decided
    what belongs in that tuple.
  Get the classification wrong, and no amount of backoff or jitter will save you 
    from hammering a service with requests that will never succeed.
"""

import random 
import time
from typing import Callable, TypeVar
from fxrates.exceptions import RateServiceTimeout, RateServiceUnavailable

T = TypeVar("T")

RETRYABLE_EXCEPTIONS = (RateServiceTimeout, RateServiceUnavailable)

def call_with_retry(func: Callable[[], T], *, 
                    max_attempts: int = 5, 
                    base_delay: float = 0.05, 
                    max_delay: float = 0.2) -> T:
    attempts = 0
    while True:
        attempts += 1
        try:
            return func()
        except RETRYABLE_EXCEPTIONS as e:
            if attempts >= max_attempts:
                raise
            backoff = min(base_delay * (2 ** (attempts - 1)), max_delay)
            # delay will include a random jitter to avoid thundering herd problems
            delay = random.uniform(0, backoff)
            print(f"  attempt {attempts} failed: {e}. Retrying in {delay:.3f} seconds...")
            time.sleep(delay)