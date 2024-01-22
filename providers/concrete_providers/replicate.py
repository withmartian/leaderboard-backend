import replicate
import os
import requests
import time
from providers.abstract_providers.base_provider import BaseProvider
import asyncio
from dotenv import load_dotenv

load_dotenv()


class Replicate(BaseProvider):
    NAME = "Replicate"
    API_KEY = os.environ["REPLICATE_API_TOKEN"]
    MODEL_TO_URL = {
        "llama2-70b-chat": "https://api.replicate.com/v1/models/meta/llama2-70b-chat/predictions",
        "mixtral-8x7b": "https://api.replicate.com/v1/models/mistralai/mixtral-8x7b-instruct-v0.1/predictions",
    }
    SUPPORTED_MODELS = {
        "llama2-70b-chat": "meta/llama-2-70b-chat",
        "mixtral-8x7b": "mistralai/mixtral-8x7b-instruct-v0.1",
    }

    async def call_sdk(self, llm_name: str, prompt: str, max_tokens: int) -> float:
        start = time.time()
        output = await replicate.async_run(
            self.SUPPORTED_MODELS[llm_name],
            input={
                "prompt": prompt,
                "max_new_tokens": max_tokens,
            },
        )
        latency = time.time() - start
        return len(list(output)) / latency

    async def call_streaming(
        self, llm_name: str, prompt: str, max_tokens: int = 5
    ) -> float:
        start = time.time()

        def sync_call_streaming():
            stream = replicate.stream(
                self.SUPPORTED_MODELS[llm_name],
                input={"prompt": prompt, "max_new_tokens": max_tokens},
            )
            for event in stream:
                if event and event.data:
                    return time.time() - start

        return await asyncio.to_thread(sync_call_streaming)
