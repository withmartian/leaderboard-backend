from abc import ABC
import time
from adapters.adapter_factory import AdapterFactory
from adapters.types import Prompt
import json


class BaseProvider(ABC):
    ADAPTER_MODEL_STR_MAP = (
        {}
    )  # maps leaderboard model name to adapter model string, which is f"{vendor_name}/{provider_name}""
    PROVIDER_NAME = None

    def get_adapter_model_str(self, llm_name: str):
        return self.ADAPTER_MODEL_STR_MAP[llm_name]

    def get_supported_models(self):
        return list(self.ADAPTER_MODEL_STR_MAP.keys())

    async def call_sdk(self, llm_name: str, prompt: str, max_tokens: int) -> float:
        adapter_str = (
            f"{self.get_provider_name().lower()}/{self.get_adapter_model_str(llm_name)}"
        )
        adapter = AdapterFactory.get_adapter_by_path(adapter_str)
        input = adapter.convert_to_input(Prompt(prompt))
        start = time.time()
        response = await adapter.execute_async(
            input, max_tokens=max_tokens, timeout=600
        )
        latency = time.time() - start
        return response.token_counts.completion / latency

    async def call_streaming(
        self, llm_name: str, prompt: str, max_tokens: int
    ) -> float:
        adapter_str = (
            f"{self.get_provider_name().lower()}/{self.get_adapter_model_str(llm_name)}"
        )
        adapter = AdapterFactory.get_adapter_by_path(adapter_str)
        input = adapter.convert_to_input(Prompt(prompt))
        start = time.time()
        adapter_response = await adapter.execute_async(
            input, max_tokens=max_tokens, stream=True, timeout=600
        )

        async for chunk in adapter_response.response:
            chunk = json.loads(chunk[6:].strip())
            if chunk["choices"][0]["delta"]["content"] is not None:
                return time.time() - start

    @classmethod
    def get_provider_name(cls) -> str:
        return cls.PROVIDER_NAME
