from datetime import datetime
from typing import List, Dict
from utils.types import ModelName, TokenCounts
from pydantic import BaseModel

from database.mongo import DatabaseClient


class Throughputs(BaseModel):
    start_time: datetime
    provider_name: str
    llm_name: ModelName
    concurrent_requests: int
    output_tokens: TokenCounts
    tokens_per_second: List[float]


class TTFT(BaseModel):
    start_time: datetime
    provider_name: str
    llm_name: ModelName
    concurrent_requests: int
    ttft: List[float]


class StaticData(BaseModel):
    provider_name: str
    url: str
    logo_url: str
    llm_name: ModelName
    cost: Dict[str, float]
    rate_limit: str


async def save_throughputs(throughputs: Throughputs) -> None:
    throughputs_collection = DatabaseClient.get_collection("throughput")
    await throughputs_collection.insert_one(throughputs.model_dump(by_alias=True))


async def save_ttft(ttfts: TTFT) -> None:
    ttft_collection = DatabaseClient.get_collection("ttft")
    await ttft_collection.insert_one(ttfts.model_dump(by_alias=True))


async def save_static_data(static_data: StaticData) -> None:
    static_data_collection = DatabaseClient.get_collection("static-data")
    await static_data_collection.insert_one(static_data.model_dump(by_alias=True))
