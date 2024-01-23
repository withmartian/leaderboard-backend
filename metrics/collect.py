from providers.provider_factory import ProviderFactory
from utils.prompts import get_prompt
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
from metrics.aggregate import aggregate_ttft, aggregate_throughputs
import itertools

NUM_WARMUP_REQUESTS = 3
CONCURRENT_REQUESTS = [50, 20, 2]
AVERAGE_OVER = 10
COLLECTION_RETRIES = 2


async def validate_and_warmup(provider_name: str, llm_name: ModelName) -> bool:
    provider = ProviderFactory.get_provider(provider_name)
    if llm_name not in provider.get_supported_models():
        return False

    # send warmup request
    warmup_request = 1 if provider_name == "Perplexity" else NUM_WARMUP_REQUESTS
    for _ in range(warmup_request):
        try:
            await provider.call_sdk(llm_name=llm_name, prompt="Hi", max_tokens=5)
        except Exception as e:
            print(
                f"Caught exception in validate_and_warmup for {provider_name} on {llm_name}: "
                + str(e)
            )
    return True


def get_sleep_time(num_concurrent_requests: int):
    return 120 if num_concurrent_requests >= 20 else 30


async def get_throughputs(
    provider_name: str,
    llm_name: ModelName,
    output_tokens: TokenCounts,
    num_concurrent_requests: int,
    num_repeats: int = 1,
):
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
        except Exception as e:
            print(
                f"**** Caught exception in get_throughput for provider={provider_name}, model={llm_name}, output_tokens={output_tokens}, concurrent_requests={num_concurrent_requests}: {str(e)}"
            )
        sleep_time = get_sleep_time(num_concurrent_requests)
        await asyncio.sleep(sleep_time)


async def get_ttft(
    provider_name: str,
    llm_name: ModelName,
    num_concurrent_requests: int,
    num_repeats: int = 1,
) -> None:
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
        except Exception as e:
            print(
                f"***** Caught exception in get_ttft for provider={provider_name}, model={llm_name}, concurrent_requests={num_concurrent_requests}: {str(e)}"
            )
        sleep_time = get_sleep_time(num_concurrent_requests)
        await asyncio.sleep(sleep_time)


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

    # collect TTFT and Throughput for combinations that hasn't already been collected within the past ~2.5h
    for combo in ttft_combinations:
        provider_name, model, num_concurrent_requests = combo

        if (
            model
            not in ProviderFactory.get_provider(provider_name).get_supported_models()
        ) or await aggregate_ttft(provider_name, model, num_concurrent_requests, 0.1):
            continue
        try:
            repeats = max(AVERAGE_OVER // num_concurrent_requests, 1)
            await get_ttft(*combo, num_repeats=repeats)
        except:
            pass
    for combo in throughput_combinations:
        provider_name, model, output_tokens, num_concurrent_requests = combo
        if (
            model
            not in ProviderFactory.get_provider(provider_name).get_supported_models()
        ) or await aggregate_throughputs(
            provider_name, model, output_tokens, num_concurrent_requests, 0.1
        ):
            continue
        try:
            repeats = max(AVERAGE_OVER // num_concurrent_requests, 1)
            await get_throughputs(*combo, num_repeats=repeats)
        except:
            pass


async def collect_metrics():
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


async def collect_metrics_with_retries():
    for _ in range(COLLECTION_RETRIES):
        await collect_metrics()
        asyncio.sleep(600)
