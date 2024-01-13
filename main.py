from providers.provider_factory import ProviderFactory
from utils.types import ModelName, TokenCounts
from metrics.collect import get_throughputs, get_ttft
import itertools
from utils.types import ModelName, TokenCounts
import asyncio
from providers.provider_factory import ProviderFactory

CONCURRENT_REQUESTS = [2, 20]  # FIXME
AVERAGE_OVER = 20


async def collect_all_metrics():
    """
    Collect throughputs and TTFT for all providers.
    """
    provider_names = ProviderFactory.get_all_provider_names()
    tasks = []
    for provider_name in provider_names:
        task = asyncio.create_task(handle_provider(provider_name))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def handle_provider(provider_name):
    """
    Handle all combinations for a specific provider.
    """
    combinations = itertools.product(
        [provider_name],
        ModelName,
        TokenCounts,
        CONCURRENT_REQUESTS,
    )

    for combo in combinations:
        concurrent_requests = combo[-1]
        try:
            repeats = max(AVERAGE_OVER // concurrent_requests, 1)
            await get_throughputs(*combo, num_repeats=repeats)
        except:
            pass


if __name__ == "__main__":
    asyncio.run(collect_all_metrics())
