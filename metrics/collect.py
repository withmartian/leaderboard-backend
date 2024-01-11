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
    RequestMethod,
)
import time


async def get_throughputs(
    provider_name: str,
    llm_name: ModelName,
    input_tokens: TokenCounts,
    output_tokens: TokenCounts,
    request_method: RequestMethod,
    num_concurrent_requests: int = 30,
):
    """
    Collect throughputs for num_concurrent requests for a  provider given a model, an input prompt, max_tokens, and a request method. Save results to DB.
    """
    provider = ProviderFactory.get_provider(provider_name)
    if llm_name not in provider.SUPPORTED_MODELS:
        return
    prompt = get_prompt(input_tokens)
    raw_throughputs = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        futures = [
            executor.submit(
                provider.get_request_method(request_method),
                llm_name=llm_name,
                prompt=prompt,
                max_tokens=output_tokens,
            )
            for _ in range(num_concurrent_requests)
        ]
        for future in concurrent.futures.as_completed(futures):
            raw_throughputs.append(future.result())

    throughputs = Throughputs(
        start_time=start_time,
        provider_name=provider_name,
        llm_name=llm_name,
        concurrent_requests=num_concurrent_requests,
        request_method=request_method,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        tokens_per_second=raw_throughputs,
    )
    await save_throughputs(throughputs)
    print(
        f"Saved throughputs for provider = {provider_name}, model = {llm_name}, input tokens = {input_tokens}, output tokens = {output_tokens}, request method = {request_method}, concurrent requests = {num_concurrent_requests}"
    )
    return raw_throughputs


async def get_ttft(
    provider_name: str,
    llm_name: ModelName,
    input_tokens: TokenCounts,
    num_concurrent_requests: int = 30,
):
    """
    Collect throughputs for num_concurrent_requests for a provider given a model, and an input prompt. Save results to DB.
    """
    provider = ProviderFactory.get_provider(provider_name)
    if llm_name not in provider.SUPPORTED_MODELS:
        return
    prompt = get_prompt(input_tokens)
    raw_ttfts = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        futures = [
            executor.submit(
                provider.get_ttft,
                llm_name=llm_name,
                prompt=prompt,
                max_tokens=10,  # number of output tokens doesn't matter since we're measuring ttft. 10 is an arbitrary small number to save cost.
            )
            for _ in range(num_concurrent_requests)
        ]
        for future in concurrent.futures.as_completed(futures):
            raw_ttfts.append(future.result())

    ttft = TTFT(
        start_time=start_time,
        provider_name=provider_name,
        llm_name=llm_name,
        concurrent_requests=num_concurrent_requests,
        input_tokens=input_tokens,
        ttft=raw_ttfts,
    )
    await save_ttft(ttft)
    return raw_ttfts
