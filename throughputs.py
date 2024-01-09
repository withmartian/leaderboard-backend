import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from provider_factory import ProviderFactory
from prompts import get_prompt
from models.throughput import Throughputs, save_throughputs, TTFT, save_ttft
import time


def get_throughputs(
    provider_name: str,
    model_name: str,
    input_tokens: int,
    output_tokens: int,
    request_method: str,
    num_concurrent_requests: int = 30,
):
    """
    Collect throughputs for num_concurrent requests for a  provider given a model, an input prompt, max_tokens, and a request method. Save results to DB.
    """
    provider = ProviderFactory.get_provider(provider_name)
    prompt = get_prompt(input_tokens)
    throughputs = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        futures = [
            executor.submit(
                provider.get_request_method(request_method),
                model_name=model_name,
                prompt=prompt,
                max_tokens=output_tokens,
            )
            for _ in range(num_concurrent_requests)
        ]
        for future in concurrent.futures.as_completed(futures):
            throughputs.append(future.result())

    throughputs = Throughputs(
        start_time=start_time,
        provider_name=provider_name,
        model_name=model_name,
        concurrent_requests=num_concurrent_requests,
        request_method=request_method,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        tokens_per_second=throughputs,
    )
    save_throughputs(throughputs)
    return throughputs


def get_ttft(
    provider_name: str,
    model_name: str,
    input_tokens: int,
    num_concurrent_requests: int = 30,
):
    """
    Collect throughputs for num_concurrent_requests for a provider given a model, and an input prompt. Save results to DB.
    """
    provider = ProviderFactory.get_provider(provider_name)
    prompt = get_prompt(input_tokens)
    ttfts = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_concurrent_requests) as executor:
        futures = [
            executor.submit(
                provider.get_ttft,
                model_name=model_name,
                prompt=prompt,
                max_tokens=10,  # number of output tokens doesn't matter since we're measuring ttft. 10 is an arbitrary small number to save cost.
            )
            for _ in range(num_concurrent_requests)
        ]
        for future in concurrent.futures.as_completed(futures):
            ttfts.append(future.result())

    ttft = TTFT(
        start_time=start_time,
        provider_name=provider_name,
        model_name=model_name,
        concurrent_requests=num_concurrent_requests,
        input_tokens=input_tokens,
        ttft=ttfts,
    )
    save_ttft(ttft)
    return ttfts
