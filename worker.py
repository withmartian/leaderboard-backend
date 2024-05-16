import asyncio
from database.mongo import DatabaseClient
from metrics.collect import collect_metrics_with_retries


async def main():
    await DatabaseClient.connect()
    await DatabaseClient.create_indexes()

    await collect_metrics_with_retries()

    await DatabaseClient.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
