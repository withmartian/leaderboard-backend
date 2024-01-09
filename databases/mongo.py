import os

from dotenv import load_dotenv
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pymongo.server_api import ServerApi

DATABASE_NAME = "provider-leaderboard"
COLLECTIONS = {"throughputs", "ttft"}

load_dotenv()


class DatabaseClient:
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase

    @classmethod
    def connect(cls):
        cls.client = AsyncIOMotorClient(
            os.environ["MONGO_URI"], server_api=ServerApi("1")
        )
        cls.db = cls.client[DATABASE_NAME]

    @classmethod
    async def disconnect(cls):
        cls.client.close()

    @classmethod
    def get_collection(cls, collection_name: str) -> AsyncIOMotorCollection:
        if collection_name not in COLLECTIONS:
            raise ValueError(f"Collection {collection_name} does not exist")
        return cls.db[collection_name]


# NOTE: database client must be connected before importing any models
DatabaseClient.connect()
