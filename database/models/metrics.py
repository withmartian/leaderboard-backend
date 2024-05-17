from datetime import datetime
from typing import List, Dict
from utils.types import ModelName, TokenCounts
from pydantic import BaseModel
from database.mongo import DatabaseClient
from database.redis import RedisClient

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
    cost: Dict[str, Dict[str, float | str]]
    rate_limit: str


async def save_throughputs(throughputs: Throughputs) -> None:
    throughputs_collection = DatabaseClient.get_collection("throughput")
    await throughputs_collection.insert_one(throughputs.model_dump(by_alias=True))
    RedisClient.save_throughput_metrics(
        throughputs.tokens_per_second,
        throughputs.provider_name,
        throughputs.llm_name,
        throughputs.concurrent_requests,
        throughputs.output_tokens
    )



async def save_ttft(ttfts: TTFT) -> None:
    ttft_collection = DatabaseClient.get_collection("ttft")
    await ttft_collection.insert_one(ttfts.model_dump(by_alias=True))
    RedisClient.save_ttft_metrics(
        ttfts.ttft, ttfts.provider_name, ttfts.llm_name, ttfts.concurrent_requests)

async def save_static_data(static_data: StaticData) -> None:
    static_data_collection = DatabaseClient.get_collection("static-data")
    await static_data_collection.insert_one(static_data.model_dump(by_alias=True))


async def get_static_data(provider_name: str) -> StaticData | None:
    static_data_collection = DatabaseClient.get_collection("static-data")
    query = {
        "provider_name": provider_name,
    }
    async for document in static_data_collection.find(query):
        return document
