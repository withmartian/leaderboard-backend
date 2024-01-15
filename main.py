from fastapi import FastAPI
from database.mongo import DatabaseClient  # Adjust the import path as needed
from utils.types import TokenCounts
from typing import List

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    DatabaseClient.connect()
    await DatabaseClient.create_indexes()


@app.on_event("shutdown")
async def shutdown_event():
    await DatabaseClient.disconnect()


# @app.get("/")
# async def get_provider_data(
#     output_tokens: TokenCounts, num_concurrent_requests: int, model_names: List[str]
# ):
