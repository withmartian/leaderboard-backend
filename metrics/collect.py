import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
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
import time
import asyncio
from typing import List


async def get_throughputs(
    provider_name: str,
    llm_name: ModelName,
    output_tokens: TokenCounts,
    num_concurrent_requests: int = 30,
) -> List[float]:
    """
    Collect throughputs for num_concurrent requests for a  provider given a model, an input prompt, max_tokens, and a request method. Save results to DB.
    """
    provider = ProviderFactory.get_provider(provider_name)
    if llm_name not in provider.get_supported_models():
        return
    prompt = get_prompt(
        100
    )  # since input tokens don't matter for throughput, use a short input prompt
    raw_throughputs = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        futures = [
            executor.submit(
                provider.call_sdk,
                llm_name=llm_name,
                prompt=prompt,
                max_tokens=output_tokens,
            )
            for _ in range(num_concurrent_requests)
        ]
        for future in concurrent.futures.as_completed(futures):
            raw_throughputs.append(future.result(timeout=120))

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
    return raw_throughputs


async def get_ttft(
    provider_name: str,
    llm_name: ModelName,
    input_tokens: TokenCounts,
    num_concurrent_requests: int = 30,
) -> List[float]:
    """
    Collect throughputs for num_concurrent_requests for a provider given a model, and an input prompt. Save results to DB.
    """
    provider = ProviderFactory.get_provider(provider_name)
    if llm_name not in provider.get_supported_models():
        return
    prompt = get_prompt(input_tokens)

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
        input_tokens=input_tokens,
        ttft=raw_ttfts,
    )
    await save_ttft(ttft)
    print(
        f"Saved TTFT for provider = {provider_name}, model = {llm_name}, input tokens = {input_tokens}, concurrent requests = {num_concurrent_requests}"
    )
    return raw_ttfts
