import asyncio

from pricing_api import fetch_price


async def check_all_prices(skus: list[str]) -> dict[str, float]:
    tasks = [fetch_price(sku) for sku in skus]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    prices = {}
    for sku, result in zip(skus, results):
        if isinstance(result, Exception):
            print(f"Failed to price {sku}: {result}")
        else:
            prices[sku] = result
    return prices
