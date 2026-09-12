import asyncio
import time

from price_checker import check_all_prices

SKUS = [f"SKU-{i:04d}" for i in range(50)]


async def main() -> None:
    start = time.perf_counter()
    prices = await check_all_prices(SKUS)
    elapsed = time.perf_counter() - start

    print(f"\nPriced {len(prices)} of {len(SKUS)} SKUs in {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
