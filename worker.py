import asyncio
from database.mongo import DatabaseClient
from metrics.collect import collect_metrics

async def main():
    await DatabaseClient.connect()
    await DatabaseClient.create_indexes()

    try:
        await collect_metrics()
    finally:
        await DatabaseClient.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
