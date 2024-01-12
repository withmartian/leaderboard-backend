from providers.provider_factory import ProviderFactory
from utils.types import ModelName, TokenCounts
from metrics.collect import get_throughputs, get_ttft
import itertools
from utils.types import ModelName, TokenCounts
import asyncio
import time
from metrics.aggregate import aggregate_throughputs, aggregate_ttft
from providers.provider_factory import ProviderFactory

CONCURRENT_REQUESTS = [2, 10]  # FIXME
NUM_WARMUP_REQUESTS = 1


async def send_warmup_requests(provider_name: str, model: ModelName):
    provider = ProviderFactory.get_provider(provider_name)
    for _ in range(NUM_WARMUP_REQUESTS):
        print(f"Sending warmup request for {provider_name} on {model}")
        await provider.call_sdk(model, "Hi!", max_tokens=10)


async def collect_all_metrics():
    """
    Collect throughputs and TTFT for all providers.
    """
    provider_names = ProviderFactory.get_all_provider_names()
    warmup_tasks = []

    for provider_name in provider_names:
        provider = ProviderFactory.get_provider(provider_name)
        for model in provider.get_supported_models():
            task = asyncio.create_task(send_warmup_requests(provider_name, model))
            warmup_tasks.append(task)

    await asyncio.gather(*warmup_tasks)

    collection_tasks = []
    for provider_name in provider_names:
        task = asyncio.create_task(handle_provider(provider_name))
        collection_tasks.append(task)

    await asyncio.gather(*collection_tasks)


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
        print(combo)
        concurrent_requests = combo[-1]
        # collect multiple times when the concurrent requests is less than the max to allow for more accurate aggregation
        for _ in range(max(CONCURRENT_REQUESTS) // concurrent_requests):
            try:
                await get_ttft(*combo)
            except Exception as e:
                print(e)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(collect_all_metrics())
