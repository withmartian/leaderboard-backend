import asyncio
import logging
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

from fastapi import BackgroundTasks, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .aws.sqs_client import receive_messages
from .database.models.metrics import get_static_data
from .database.mongo import DatabaseClient
from .metrics.aggregate import aggregate_throughputs, aggregate_ttft
from .metrics.collect import collect_metrics_with_retries
from .providers.provider_factory import ProviderFactory
from .settings import settings
from .utils.types import ModelName, TokenCounts


CACHE_EXPIRATION = timedelta(days=settings.cache_expiration_in_days)
HOURS_BETWEEN_COLLECTIONS = settings.hours_between_collections

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: clean up local scheduler
scheduler = AsyncIOScheduler()
query_cache: Dict[str, Tuple[Any, datetime]] = {}


async def schedule_daily_collections():
    # Generate two random times that are at least HOURS_BETWEEN_COLLECTIONS apart
    time1 = random.randint(0, 23 - HOURS_BETWEEN_COLLECTIONS)
    time2 = (time1 + random.randint(HOURS_BETWEEN_COLLECTIONS, 23 - time1)) % 24

    # Clear existing jobs
    for job in scheduler.get_jobs():
        if job.id.startswith("daily_collection"):
            job.remove()

    scheduler.add_job(
        collect_metrics_with_retries,
        trigger=CronTrigger(hour=time1, minute=0),
        id="daily_collection_1",
    )
    scheduler.add_job(
        collect_metrics_with_retries,
        trigger=CronTrigger(hour=time2, minute=0),
        id="daily_collection_2",
    )


@app.on_event("startup")
async def startup_event():
    await DatabaseClient.connect()
    await DatabaseClient.create_indexes()
    # scheduler.add_job(
    #     schedule_daily_collections,
    #     trigger=CronTrigger(hour=0, minute=0),
    # )
    # scheduler.start()

    BackgroundTasks().add_task(receive_messages)


@app.on_event("shutdown")
async def shutdown_event():
    await DatabaseClient.disconnect()


@app.get("/")
def root():
    return {"message": "Provider Leaderboard is up and running!"}


def generate_cache_key(
    output_tokens, num_concurrent_request, selected_models, num_days
):
    return f"{output_tokens}-{num_concurrent_request}-{','.join(selected_models)}-{num_days}"


def is_cache_expired(
    timestamp: datetime, expiry_duration: timedelta = CACHE_EXPIRATION
) -> bool:
    return datetime.now() - timestamp > expiry_duration


@app.get("/get-provider-data")
async def get_provider_data(
    output_tokens: TokenCounts = Query(...),
    num_concurrent_request: int = Query(...),
    selected_models: List[str] = Query([]),
    num_days: int = Query(5),
):
    if not selected_models:
        return []

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

    # check if query exists in cache
    cache_key = generate_cache_key(
        output_tokens, num_concurrent_request, selected_models, num_days
    )
    if cache_key in query_cache and not is_cache_expired(query_cache[cache_key][1]):
        return query_cache[cache_key][0]

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

    tasks = [
        query_provider_model(provider_name, model)
        for provider_name in ProviderFactory.get_all_provider_names()
        for model in ProviderFactory.get_provider(provider_name).get_supported_models()
    ]

    results = await asyncio.gather(*tasks)
    output = [result for result in results if result]
    query_cache[cache_key] = (output, datetime.now())
    return output
