"""Chunked, generator-based processing for a catalog too large to
sensibly hand to asyncio.gather all at once.

The semaphore in price_checker.py bounds how many requests can be IN
FLIGHT at the same time. It does NOT bound how many task objects get
CREATED up front - asyncio.gather(*[...]) still builds the entire list
of tasks before running any of them. For 50 SKUs that's nothing. For a
catalog of hundreds of thousands, building every task object at once,
before any of them even start, is a real memory cost on its own -
separate from, and in addition to, the concurrency problem.

Chunking fixes this different problem: process the catalog in bounded
batches, so at any moment only one batch's worth of tasks exists at
all - not the whole catalog's.
"""

from collections.abc import Iterable, Iterator

from pricecheck.price_checker import check_all_prices

CHUNK_SIZE = 50


def iter_sku_chunks(skus: Iterable[str], chunk_size: int = CHUNK_SIZE) -> Iterator[list[str]]:
    """Yields successive chunks of `chunk_size` SKUs, one at a time.

    `skus` can itself be a generator - this never materializes the
    whole catalog into memory, whether it's 500 SKUs or 500,000.
    """
    chunk: list[str] = []
    for sku in skus:
        chunk.append(sku)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


async def check_full_catalog(
    skus: Iterable[str], chunk_size: int = CHUNK_SIZE
) -> dict[str, float]:
    """Processes an entire catalog, chunk by chunk. Within each chunk,
    check_all_prices still applies its own bounded concurrency - the
    two techniques stack, they don't replace each other.
    """
    all_prices: dict[str, float] = {}
    for chunk_number, chunk in enumerate(iter_sku_chunks(skus, chunk_size), start=1):
        print(f"Processing chunk {chunk_number} ({len(chunk)} SKUs)...")
        chunk_prices = await check_all_prices(chunk)
        all_prices.update(chunk_prices)
    return all_prices
