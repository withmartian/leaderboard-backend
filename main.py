from fastapi import FastAPI, Query
from database.mongo import DatabaseClient  # Adjust the import path as needed
from utils.types import TokenCounts
from typing import List
from metrics.aggregate import aggregate_throughputs, aggregate_ttft
from providers.provider_factory import ProviderFactory
from utils.types import ModelName
from database.models.metrics import get_static_data
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from metrics.collect import collect_metrics_with_retries
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    await DatabaseClient.connect()
    await DatabaseClient.create_indexes()
    scheduler.add_job(
        collect_metrics_with_retries,
        trigger=IntervalTrigger(days=1),
    )
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    await DatabaseClient.disconnect()


@app.get("/")
def root():
    return {"message": "Provider Leaderboard is up and running!"}


@app.get("/get-provider-data")
async def get_provider_data(
    output_tokens: TokenCounts = Query(...),
    num_concurrent_request: int = Query(...),
    selected_models: List[str] = Query(...),
    num_days: int = Query(5),
):
    async def query_provider_model(provider_name, model):
        if model not in model_names:
            return None

        throughput, ttft, static_data = await asyncio.gather(
            aggregate_throughputs(
                provider_name, model, output_tokens, num_concurrent_request, num_days
            ),
            aggregate_ttft(provider_name, model, num_concurrent_request, num_days),
            get_static_data(provider_name),
        )

        if not throughput or not ttft:
            return None

        return {
            "provider": provider_name,
            "url": static_data.get("url"),
            "logo_url": static_data.get("logo_url"),
            "model": model,
            "cost": static_data.get("cost")[model],
            "rate_limit": static_data.get("rate_limit"),
            "throughput": throughput,
            "ttft": ttft,
        }

    model_names = []
    if "llama2-70b-chat" in selected_models:
        model_names.append(ModelName.LLAMA2_70B_CHAT.value)
    if "mixtral-8x7b" in selected_models:
        model_names.append(ModelName.MIXTRAL_8X7B.value)
    if "OpenAI models" in selected_models:
        model_names.extend(
            [
                ModelName.GPT4.value,
                ModelName.GPT4_TURBO.value,
                ModelName.GPT3_TURBO.value,
            ]
        )
    if "Anthropic models" in selected_models:
        model_names.extend([ModelName.CLAUDE2.value, ModelName.CLAUDE_INSTANT.value])
    if not model_names:
        return []
    tasks = [
        query_provider_model(provider_name, model)
        for provider_name in ProviderFactory.get_all_provider_names()
        for model in ProviderFactory.get_provider(provider_name).get_supported_models()
    ]

    results = await asyncio.gather(*tasks)
    return [result for result in results if result]
