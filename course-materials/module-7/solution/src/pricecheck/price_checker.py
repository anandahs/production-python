"""Bounded fan-out. The fix is the semaphore - it caps how many
fetch_price calls can genuinely be in flight at once, so we never
exceed what the real service can actually handle, no matter how many
SKUs we're asked to price.
"""

import asyncio

from pricecheck.pricing_api import fetch_price

# Set below the service's real limit (5), not at it - a small safety
# margin, not an arbitrary round number.
MAX_CONCURRENT_REQUESTS = 4


async def _fetch_one(semaphore: asyncio.Semaphore, sku: str) -> tuple[str, float | Exception]:
    async with semaphore:
        try:
            price = await fetch_price(sku)
            return sku, price
        except Exception as e:
            return sku, e


async def check_all_prices(skus: list[str]) -> dict[str, float]:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    tasks = [_fetch_one(semaphore, sku) for sku in skus]
    results = await asyncio.gather(*tasks)

    prices: dict[str, float] = {}
    for sku, result in results:
        if isinstance(result, Exception):
            print(f"Failed to price {sku}: {result}")
        else:
            prices[sku] = result
    return prices
