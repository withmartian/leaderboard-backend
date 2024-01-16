from providers.provider_factory import ProviderFactory
from prompts import get_prompt
from database.models.metrics import (
    Throughputs,
    save_throughputs,
    TTFT,
    save_ttft,
    TokenCounts,
    ModelName,
)
from utils.types import ModelName
import time
import asyncio
from typing import List, Callable
import itertools

NUM_WARMUP_REQUESTS = 3
CONCURRENT_REQUESTS = [20, 2]  # FIXME
AVERAGE_OVER = 10


async def validate_and_warmup(provider_name: str, llm_name: ModelName) -> bool:
    provider = ProviderFactory.get_provider(provider_name)
    if llm_name not in provider.get_supported_models():
        return False

    # send warmup request
    warmup_request = (
        1
        if provider_name == "Perplexity" or provider_name == "Lepton"
        else NUM_WARMUP_REQUESTS
    )
    for _ in range(warmup_request):
        await provider.call_sdk(llm_name=llm_name, prompt="Hi", max_tokens=5)
    return True


def get_sleep_time(provider_name: str, num_concurrent_requests: int):
    if (
        provider_name == "Perplexity"
        or provider_name == "Lepton"
        or num_concurrent_requests >= 20
    ):
        return 60
    return 5


async def get_throughputs(
    provider_name: str,
    llm_name: ModelName,
    output_tokens: TokenCounts,
    num_concurrent_requests: int = 30,
    num_repeats: int = 1,
) -> List[float]:
    """
    Collect throughputs for num_concurrent requests for a  provider given a model, an input prompt, max_tokens, and a request method. Save results to DB.
    """
    provider = ProviderFactory.get_provider(provider_name)
    if not await validate_and_warmup(provider_name, llm_name):
        return
    print(
        f"Getting throughputs for provider={provider_name}, model={llm_name}, concurrent_requests={num_concurrent_requests}, output_tokens={output_tokens}, for {num_repeats} repeats"
    )

    # collect throughputs for num_repeats times
    for _ in range(num_repeats):
        try:
            prompt = get_prompt()
            start_time = time.time()
            tasks = [
                provider.call_sdk(
                    llm_name=llm_name, prompt=prompt, max_tokens=output_tokens
                )
                for _ in range(num_concurrent_requests)
            ]
            raw_throughputs = await asyncio.gather(*tasks)

            throughputs = Throughputs(
                start_time=start_time,
                provider_name=provider_name,
                llm_name=llm_name,
                concurrent_requests=num_concurrent_requests,
                output_tokens=output_tokens,
                tokens_per_second=raw_throughputs,
            )
            await save_throughputs(throughputs)
            print(
                f"Saved throughputs for provider = {provider_name}, model = {llm_name},  output tokens = {output_tokens}, concurrent requests = {num_concurrent_requests}"
            )
            sleep_time = get_sleep_time(provider_name, num_concurrent_requests)
            await asyncio.sleep(sleep_time)
        except Exception as e:
            print(
                f"**** Caught exception in get_throughput for provider={provider_name}, model={llm_name}, output_tokens={output_tokens}, concurrent_requests={num_concurrent_requests}: {str(e)}"
            )
    return raw_throughputs


async def get_ttft(
    provider_name: str,
    llm_name: ModelName,
    num_concurrent_requests: int = 30,
    num_repeats: int = 1,
) -> List[float]:
    """
    Collect throughputs for num_concurrent_requests for a provider given a model, and an input prompt. Save results to DB.
    """
    provider = ProviderFactory.get_provider(provider_name)
    if not await validate_and_warmup(provider_name, llm_name):
        return
    print(
        f"Getting TTFT for provider={provider_name}, model={llm_name}, concurrent_requests={num_concurrent_requests}, for {num_repeats} repeats"
    )

    # collect ttft for num_repeats times
    for _ in range(num_repeats):
        try:
            prompt = get_prompt()
            start_time = time.time()
            tasks = [
                provider.call_streaming(llm_name=llm_name, prompt=prompt, max_tokens=5)
                for _ in range(num_concurrent_requests)
            ]
            raw_ttfts = await asyncio.gather(*tasks)

            ttft = TTFT(
                start_time=start_time,
                provider_name=provider_name,
                llm_name=llm_name,
                concurrent_requests=num_concurrent_requests,
                ttft=raw_ttfts,
            )
            await save_ttft(ttft)
            print(
                f"Saved TTFT for provider = {provider_name}, model = {llm_name}, concurrent requests = {num_concurrent_requests}"
            )
            sleep_time = get_sleep_time(provider_name, num_concurrent_requests)
            await asyncio.sleep(sleep_time)
        except Exception as e:
            print(
                f"***** Caught exception in get_ttft for provider={provider_name}, model={llm_name}, concurrent_requests={num_concurrent_requests}: {str(e)}"
            )
    return raw_ttfts


async def provider_handler(provider_name: str, model_name: str):
    ttft_combinations = itertools.product(
        [provider_name],
        [model_name],
        CONCURRENT_REQUESTS,
    )
    throughput_combinations = itertools.product(
        [provider_name],
        [model_name],
        TokenCounts,
        CONCURRENT_REQUESTS,
    )
    for combo in ttft_combinations:
        concurrent_requests = combo[-1]
        try:
            repeats = max(AVERAGE_OVER // concurrent_requests, 1)
            await get_ttft(*combo, num_repeats=repeats)
        except:
            pass
    for combo in throughput_combinations:
        concurrent_requests = combo[-1]
        try:
            repeats = max(AVERAGE_OVER // concurrent_requests, 1)
            await get_throughputs(*combo, num_repeats=repeats)
        except:
            pass


async def collect_all_metrics():
    """
    Collect throughputs and TTFT for all providers.
    """
    provider_names = ProviderFactory.get_all_provider_names()
    tasks = []
    for provider_name in provider_names:
        for model in ModelName:
            task = asyncio.create_task(provider_handler(provider_name, model))
            tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(collect_all_metrics())
