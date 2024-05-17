import os
import numpy as np
import redis
from dotenv import load_dotenv
from utils.types import ModelName, TokenCounts
load_dotenv()


class RedisClient:
    db = redis.Redis(
        host=os.environ.get("REDIS_HOST", "router-backend-redis-1"),
        port=int(os.environ.get("REDIS_PORT", 6379)),
        password=os.environ.get("REDIS_PASSWORD", None),
        db=int(os.environ.get("REDIS_DB", 0)),
        ssl=os.environ.get("ENV", "development") == "production",
    )

    @classmethod
    def save_ttft_metrics(cls, ttfts: list[float], provider_name: str, llm_name: ModelName, concurrent_requests: int) -> str:
        key = f"ttft:{provider_name}:{llm_name.value}:{concurrent_requests}"
        metrics = {
            "p50": np.percentile(ttfts, 50),
            "p90": np.percentile(ttfts, 90)
        }
        cls.db.hmset(key, metrics)


    @classmethod
    def save_throughput_metrics(cls, throughputs: list[float], provider_name: str, llm_name: ModelName, concurrent_requests: int, output_tokens: TokenCounts) -> str:
        key = f"throughput:{provider_name}:{llm_name.value}:{concurrent_requests}:{output_tokens.value}"
        metrics = {
            "p50": np.percentile(throughputs, 50),
            "p90": np.percentile(throughputs, 90)
        }
        cls.db.hmset(key, metrics)
