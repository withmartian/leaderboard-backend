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
    HTTP_URL = None
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

    def call_http(
        self,
        llm_name: str,
        prompt: str,
        max_tokens: int,
        url: str = None,
        get_completion_tokens: Callable = default_get_completion_tokens,
    ) -> float:
        url = url or self.HTTP_URL
        data = {
            "model": self.SUPPORTED_MODELS[llm_name],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json",
        }
        try:
            start = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=60)
            latency = time.time() - start
            response = response.json()
            return get_completion_tokens(response) / latency
        except Exception as e:
            print(e)

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
            timeout=180,
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
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                return time.time() - start
