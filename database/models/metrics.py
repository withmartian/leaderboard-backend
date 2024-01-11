from datetime import datetime
from typing import List
from utils.types import ModelName, RequestMethod, TokenCounts

from pydantic import BaseModel

from database.mongo import DatabaseClient


class Throughputs(BaseModel):
    start_time: datetime
    provider_name: str
    llm_name: ModelName
    concurrent_requests: int
    request_method: RequestMethod
    input_tokens: TokenCounts
    output_tokens: TokenCounts
    tokens_per_second: List[float]


class TTFT(BaseModel):
    start_time: datetime
    provider_name: str
    llm_name: ModelName
    concurrent_requests: int
    input_tokens: TokenCounts
    ttft: List[float]


async def save_throughputs(throughputs: Throughputs) -> None:
    throughputs_collection = DatabaseClient.get_collection("throughput")
    await throughputs_collection.insert_one(throughputs.model_dump(by_alias=True))


async def save_ttft(ttfts: TTFT) -> None:
    ttft_collection = DatabaseClient.get_collection("ttft")
    await ttft_collection.insert_one(ttfts.model_dump(by_alias=True))
