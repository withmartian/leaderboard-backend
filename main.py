import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from provider_factory import ProviderFactory
from prompts import get_prompt
from models.throughput import (
    Throughputs,
    save_throughputs,
    TTFT,
    save_ttft,
    TokenCounts,
    ModelName,
    RequestMethod,
)
import time
import numpy as np
from typing import List, Dict
from databases.mongo import DatabaseClient
from datetime import datetime, timedelta


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


async def aggregate_throughputs(
    provider_name: str,
    llm_name: ModelName,
    num_days: int,
    input_tokens: TokenCounts,
    output_tokens: TokenCounts,
    concurrent_requests: int,
    request_method: RequestMethod,
) -> Dict[str, float]:
    """
    Aggregate throughputs for a provider over the past num_days given a model, an input prompt length, max_tokens, and a request method.
    Return the P50 and P90 of the throughputs in a dictionary.
    """
    throughputs_collection = DatabaseClient.get_collection("throughput")
    start = datetime.now() - timedelta(days=num_days)
    query = {
        "start_time": {"$gte": start},
        "provider_name": provider_name,
        "llm_name": llm_name,
        "concurrent_requests": concurrent_requests,
        "request_method": request_method,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }
    all_throughputs = []
    async for document in throughputs_collection.find(query):
        all_throughputs.extend(document.get("tokens_per_second"))

    if len(all_throughputs) == 0:
        raise Exception(f"No entry is found in the throughput collection.")

    return {
        "p50": np.percentile(all_throughputs, 50),
        "p90": np.percentile(all_throughputs, 90),
    }


async def aggregate_ttft(
    provider_name: str,
    llm_name: ModelName,
    num_days: int,
    input_tokens: TokenCounts,
    concurrent_requests: int,
) -> Dict[str, float]:
    """
    Aggregate TTFT for a provider over the past num_days given a model, an input prompt length, max_tokens, and a request method.
    Return the P50 and P90 of the TTFT in a dictionary.
    """
    ttft_collection = DatabaseClient.get_collection("ttft")
    start = datetime.now() - timedelta(days=num_days)
    query = {
        "start_time": {"$gte": start},
        "provider_name": provider_name,
        "llm_name": llm_name,
        "concurrent_requests": concurrent_requests,
        "input_tokens": input_tokens,
    }
    all_ttft = []
    async for document in ttft_collection.find(query):
        all_ttft.extend(document.get("ttft"))

    if len(all_ttft) == 0:
        raise Exception(f"No entry is found in the ttft collection.")

    return {
        "p50": np.percentile(all_ttft, 50),
        "p90": np.percentile(all_ttft, 90),
    }
