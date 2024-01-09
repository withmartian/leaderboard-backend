import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from provider_factory import ProviderFactory
from prompts import get_prompt
from models.throughput import Throughputs, save_throughputs
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
    Send 30 concurrent requests and save all request times and output token counts to the DB
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
        concurrent_requests=num_concurrent_requests,
        model_name=model_name,
        request_method=request_method,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        tokens_per_second=throughputs,
    )
    save_throughputs(throughputs)
    return throughputs
