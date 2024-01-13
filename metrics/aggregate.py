from database.models.metrics import (
    TokenCounts,
    ModelName,
)
import numpy as np
from typing import Dict
from database.mongo import DatabaseClient
from datetime import datetime, timedelta


async def aggregate_throughputs(
    provider_name: str,
    llm_name: ModelName,
    output_tokens: TokenCounts,
    concurrent_requests: int,
    num_days: int,
) -> Dict[str, float] | None:
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
        "output_tokens": output_tokens,
    }
    all_throughputs = []
    async for document in throughputs_collection.find(query):
        all_throughputs.extend(document.get("tokens_per_second"))

    if len(all_throughputs) > 0:
        return {
            "p50": np.percentile(all_throughputs, 50),
            "p90": np.percentile(all_throughputs, 90),
        }


async def aggregate_ttft(
    provider_name: str,
    llm_name: ModelName,
    concurrent_requests: int,
    num_days: int,
) -> Dict[str, float] | None:
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
    }
    all_ttft = []
    async for document in ttft_collection.find(query):
        all_ttft.extend(document.get("ttft"))

    if len(all_ttft) > 0:
        return {
            "p50": np.percentile(all_ttft, 50),
            "p90": np.percentile(all_ttft, 90),
        }
