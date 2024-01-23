import anthropic
import os
import requests
import time
from providers.abstract_providers.base_provider import BaseProvider

from dotenv import load_dotenv

load_dotenv()


class AnthropicProvider(BaseProvider):
    NAME = "Anthropic"
    API_KEY = os.environ["ANTHROPIC_API_KEY"]
    SUPPORTED_MODELS = {
        "claude-2.1": "claude-2.1",
        "claude-instant-1.2": "claude-instant-1.2",
    }
    CLIENT = anthropic.AsyncAnthropic(api_key=API_KEY)

    async def call_sdk(self, llm_name: str, prompt: str, max_tokens: int) -> int:
        start = time.time()
        response = await self.CLIENT.completions.create(
            model=self.SUPPORTED_MODELS[llm_name],
            max_tokens_to_sample=max_tokens,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            timeout=600,
        )
        latency = time.time() - start
        return await self.CLIENT.count_tokens(response.completion) / latency

    async def call_streaming(
        self, llm_name: str, prompt: str, max_tokens: int
    ) -> float:
        start = time.time()
        stream = await self.CLIENT.completions.create(
            model=self.SUPPORTED_MODELS[llm_name],
            max_tokens_to_sample=max_tokens,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            stream=True,
            timeout=600,
        )
        async for chunk in stream:
            if chunk.completion is not None:
                return time.time() - start
