import anthropic
import os
import requests
import time
from providers.abstract_providers.base_provider import BaseProvider

from dotenv import load_dotenv

load_dotenv()


class AnthropicProvider(BaseProvider):
    NAME = "anthropic"
    API_KEY = os.environ["ANTHROPIC_API_KEY"]
    SUPPORTED_MODELS = {
        "claude-2.1": "claude-2.1",
        "claude-instant-1.2": "claude-instant-1.2",
    }
    HTTP_URL = "https://api.anthropic.com/v1/complete"
    CLIENT = anthropic.Anthropic(api_key=API_KEY)

    def call_http(
        self,
        llm_name: str,
        prompt: str,
        max_tokens: int,
        url: str = None,
    ) -> int:
        data = {
            "model": self.SUPPORTED_MODELS[llm_name],
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": max_tokens,
        }
        headers = {
            "x-api-key": self.API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        start = time.time()
        response = requests.post(self.HTTP_URL, headers=headers, json=data)
        latency = time.time() - start
        response = response.json()
        return self.CLIENT.count_tokens(response["completion"]) / latency

    def call_sdk(self, llm_name: str, prompt: str, max_tokens: int) -> int:
        start = time.time()
        response = self.CLIENT.completions.create(
            model=self.SUPPORTED_MODELS[llm_name],
            max_tokens_to_sample=max_tokens,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
        )
        latency = time.time() - start
        return self.CLIENT.count_tokens(response.completion) / latency

    def get_ttft(self, llm_name: str, prompt: str, max_tokens: int) -> float:
        start = time.time()
        stream = self.CLIENT.completions.create(
            model=self.SUPPORTED_MODELS[llm_name],
            max_tokens_to_sample=max_tokens,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            stream=True,
        )
        for chunk in stream:
            if chunk.completion is not None:
                return time.time() - start
