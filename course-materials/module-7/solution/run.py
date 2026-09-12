import asyncio
import time
from collections.abc import Iterator

from pricecheck.catalog import check_full_catalog
from pricecheck.price_checker import check_all_prices

SKUS = [f"SKU-{i:04d}" for i in range(50)]


def generate_large_catalog(count: int) -> Iterator[str]:
    """A lazy generator standing in for 'read a huge catalog from
    somewhere' - a file, a database cursor, an API. The point is that
    this never becomes one big list in memory.
    """
    for i in range(count):
        yield f"CATALOG-SKU-{i:06d}"


async def main() -> None:
    start = time.perf_counter()
    prices = await check_all_prices(SKUS)
    elapsed = time.perf_counter() - start
    print(f"Priced {len(prices)} of {len(SKUS)} SKUs in {elapsed:.2f}s\n")

    print("Now processing a much larger catalog, in chunks...")
    start = time.perf_counter()
    large_catalog = generate_large_catalog(500)
    catalog_prices = await check_full_catalog(large_catalog, chunk_size=50)
    elapsed = time.perf_counter() - start
    print(f"\nPriced {len(catalog_prices)} of 500 catalog SKUs in {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
