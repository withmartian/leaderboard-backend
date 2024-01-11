from providers.provider_factory import ProviderFactory
from utils.types import ModelName, RequestMethod, TokenCounts
from metrics.collect import get_throughputs, get_ttft
import itertools
from utils.types import ModelName, RequestMethod, TokenCounts
import asyncio
import time

MAX_ATTEMPTS = 2
CONCURRENT_REQUESTS = [1, 10, 30]  # FIXME


async def collect_all_metrics():
    """
    Collect throughputs and TTFT for all providers.
    """
    provider_names = ProviderFactory.get_all_provider_names()
    combinations = itertools.product(
        provider_names,
        ModelName,
        TokenCounts,
        TokenCounts,
        RequestMethod,
        CONCURRENT_REQUESTS,
    )
    for combo in combinations:
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                await get_throughputs(*combo)
                break
            except Exception as e:
                attempts += 1
                print(
                    f"Attempt {attempts} - Error in collecting throughputs for combination {combo}: ",
                    e,
                )
                time.sleep(10)


if __name__ == "__main__":
    asyncio.run(collect_all_metrics())
