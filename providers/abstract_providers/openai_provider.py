from .base_provider import BaseProvider
from typing import Callable
import requests
import time
import openai


class OpenaiProvider(BaseProvider):
    """
    This class implements methods for providers that follow the openai format.
    """

    API_KEY = None
    OPENAI_BASE_URL = None
    CLIENT = None
    SUPPORTED_MODELS = None

    def __init__(self):
        if self.API_KEY and self.OPENAI_BASE_URL:
            self.CLIENT = openai.AsyncOpenAI(
                api_key=self.API_KEY,
                base_url=self.OPENAI_BASE_URL,
            )

    @staticmethod
    def default_get_completion_tokens(response: dict):
        return response["usage"]["completion_tokens"]

    async def call_sdk(
        self, llm_name: str, prompt: str, max_tokens: int, client=None
    ) -> float:
        client = client or self.CLIENT
        start = time.time()
        response = await client.chat.completions.create(
            model=self.SUPPORTED_MODELS[llm_name],
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_tokens=max_tokens,
            timeout=600,
        )
        latency = time.time() - start
        return response.usage.completion_tokens / latency

    async def call_streaming(
        self, llm_name: str, prompt: str, max_tokens: int, client=None
    ) -> float:
        client = client or self.CLIENT
        start = time.time()
        stream = await client.chat.completions.create(
            model=self.SUPPORTED_MODELS[llm_name],
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=max_tokens,
            timeout=600,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                return time.time() - start
