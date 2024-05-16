import asyncio
from metrics.collect import collect_metrics_with_retries


if __name__ == "__main__":
    asyncio.run(collect_metrics_with_retries())
